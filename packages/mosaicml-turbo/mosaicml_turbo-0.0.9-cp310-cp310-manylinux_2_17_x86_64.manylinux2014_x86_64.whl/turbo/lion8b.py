# Copyright 2022 MosaicML LLM Foundry authors
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

import numpy as np
import torch

_DTYPE_WIDTHS = {
    torch.int8: 8,
    torch.uint8: 8,
    torch.int16: 16,
    torch.float16: 16,
    torch.bfloat16: 16,
    torch.float32: 32,
}


class _CompressedOptimizer(torch.optim.Optimizer, abc.ABC):
    """LION optimizer with ~8 bits of state per parameter.

    This optimizer is a drop-in replacement for our regular LION optimizer
    with decoupled weight decay, but uses less memory, writes smaller
    checkpoints, and offers almost-numerically-identical convergence.

    Its state saved per parameter is just an int8, though there are auxiliary
    scaling factors that bring the total memory per parameter to ~8.5 bits.
    The exact quantization scheme is considered an implementation detail
    and may change.

    When training on CPUs, however, no quantization will actually take place.

    See the LION paper (https://arxiv.org/abs/2302.06675) for details about
    the algorithm itself.

    Args:
        params: iterable of parameters to optimize or dicts defining
            parameter groups
        lr: learning rate
        betas: two coefficients between 0 and 1 used to combine the current
            gradients and the momentum. The first coefficient is the weight
            of the gradient when computing the update. The second is the
            weight of the gradient when computing the new momentum.
        weight decay: Weights are multiplied by 1 - `weight_decay` after
            each optimizer step. Note that we use decoupled weight decay,
            meaning that this decay does not contribute to the momentum.
        compress_state_dict: if True, this optimizer's `state_dict` will
            include quantized optimizer states. Otherwise, the optimizer
            states are converted to bfloat16 Tensors matching the shapes of
            their corresponding parameters. The former uses ~8.5 bits per
            parameter while the latter uses 16 bits per parameter. However,
            the former is less thoroughly tested and will not work with
            FSDP or other weight sharding approaches.
        quantize: If False, optimizer states will not actually be quantized.
            This option is available so that one can easily debug whether
            the quantization is causing any convergence issues. Because
            quantization is only supported for CUDA parameters, attempting to
            update a non-CUDA tensor will raise an error.
        master_weight_bytes: If greater than the number of bytes per scalar
            in a parameter tensor, the parameter will get an auxiliary
            error correction tensor ('errors') of bytewidth equal to the
            difference. This tensor lets the optimizer closely approximate
            the semantics of using master weights of width
            `master_weight_bytes`. The content of this tensor is opaque and
            considered an implementation detail.
        check_numerics: If true, will check the standard deviations of
            parameters, the current learning rate, the param dtype, and
            `master_weight_bytes` at each step to determine if steps are
            too small to alter the weights. To avoid runtime overhead, the
            standard deviation of each weight tensor is only computed during
            the first step and load_state_dict().

    .. NOTE:

        Because `check_numerics` recomputes the parameter standard deviations
        during load_state_dict(), it is possible that saving and reloading a
        checkpoint might result in a new `LinAlgError` error appearing. Call
        recompute_param_stats() before saving a checkpoint to avoid this
        discrepancy, or simply set `check_numerics=False`.

    Raises:
        ValueError - If the hyperparameters fail sanity checks, such as
            having a learning rate greater than zero.
        NotImplementedError - If any of `quantize`, `compress_state_dict`,
            or `error_correction` are `True` and either a) there is no CUDA
            device, or b) step() is executed on a non-CUDA parameter.
        torch.linalg.LinAlgError - If check_numerics is True and estimates
            that the learning rate is too small to alter the weights.
    """

    _INTERNAL_STATE_KEYS = {
        'param_dtype', 'param_std', 'errors', 'error_dtype', 'numel'
    }

    def __init__(self,
                 params: Iterable[torch.Tensor],
                 lr: float = 1e-3,
                 betas: Tuple[float, float] = (0.9, 0.99),
                 weight_decay: float = 0,
                 quantize: bool = True,
                 compress_state_dict: bool = False,
                 master_weight_bytes: int = 4,
                 check_numerics: bool = True,
                 _fused: bool = True):  # XXX this flag is mostly for testing...

        if lr < 0.0:
            raise ValueError('Invalid learning rate: {}'.format(lr))
        if not 0.0 <= betas[0] <= 1.0:
            raise ValueError('Invalid beta parameter at index 0: {}'.format(
                betas[0]))
        if not 0.0 <= betas[1] <= 1.0:
            raise ValueError('Invalid beta parameter at index 1: {}'.format(
                betas[1]))
        if not 0.0 <= weight_decay:
            raise ValueError(
                'Invalid weight_decay value: {}'.format(weight_decay))
        _VALID_MASTER_WEIGHT_BYTES = (0, 3, 4)
        if master_weight_bytes not in _VALID_MASTER_WEIGHT_BYTES:
            raise ValueError(
                f'Master weight byte count {master_weight_bytes} ' +
                f'invalid; must be one of {_VALID_MASTER_WEIGHT_BYTES}')

        if not torch.cuda.is_available():
            needs_cuda = ' requires a CUDA device.'
            if quantize:
                raise NotImplementedError('Quantization' + needs_cuda)
            if compress_state_dict:
                raise NotImplementedError('Quantized state dict' + needs_cuda)

        self._fused = _fused and quantize
        self._quantize = quantize
        self._master_weight_bits = 8 * master_weight_bytes
        self._compress_state_dict = compress_state_dict
        self._check_numerics = check_numerics
        defaults = {
            'lr': lr,
            'initial_lr': lr,
            'betas': betas,
            'weight_decay': weight_decay,
            'fused': self._fused,
        }
        super().__init__(params, defaults)

    @abc.abstractmethod
    def _quantized_state_keys(self) -> Tuple[str, ...]:
        ...

    @torch.no_grad()
    def step(self, closure: Optional[Callable] = None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                self.step_param(p, group)
        return loss

    def recompute_param_stats(self) -> None:
        """Writes each parameter's standard deviation to its state dict."""
        for group in self.param_groups:
            for p in group['params']:
                std = float(p.detach().std().float().cpu())
                self.state[p]['param_std'] = std

    def step_param(self, p: torch.Tensor, hparams: Dict[str, Any]) -> None:
        """Performs the optimizer step on a given parameter.

        Args:
            p: The parameter to update. Must be part of one of this optimizer's
                parameter groups
            hparams: Dictionary of arguments to pass to the optimization logic;
                should be taken from the associated parameter group.
        """
        if not p.requires_grad or p.grad is None:
            return
        if self._quantize and not p.is_cuda:
            raise NotImplementedError(
                f'Can\'t use quantization with param on {p.device} ' +
                f'({p.shape}, {p.dtype}). If you need to use this class ' +
                'without a CUDA device, try creating it with ' +
                'quantize=False, master_weight_bytes=0.')
        state = self.state[p]  # type:ignore using tensor as key
        self._ensure_state_initialized(p, state)

        if self._check_numerics:
            self._check_param_numerics(p, lr=hparams['lr'])

        param_tensor = p
        errors: Optional[torch.Tensor] = None
        bitwidth = _DTYPE_WIDTHS[state['param_dtype']]
        num_err_bits = self._master_weight_bits - bitwidth
        if 'errors' in state:
            errors = state['errors']
            assert errors is not None  # pyright
            if num_err_bits == 8:
                errors = errors.view(torch.uint8)[:p.numel()].view(p.shape)
            elif num_err_bits == 16:
                errors = errors.view(dtype=torch.int16).view(p.shape)
            else:  # step master weights directly
                param_tensor = errors.view(dtype=torch.float32)
                errors = None

        decay_factor = hparams['weight_decay']
        decay_factor *= hparams['lr'] / hparams['initial_lr']

        algo_state = {
            k: v
            for k, v in state.items()
            if k not in DecoupledLionW_8bit._INTERNAL_STATE_KEYS
        }
        self._do_step(param=param_tensor,
                      grad=p.grad,
                      errors=errors,
                      weight_decay=decay_factor,
                      state=algo_state,
                      hparams=hparams)

        if param_tensor is not p:  # we stepped separate master weights
            p.copy_(param_tensor)

    def __setstate__(self, state: Dict[str, Dict[str, Any]]) -> None:
        opt_state, _ = state.values()  # other val is param_groups
        for param in opt_state:
            assert isinstance(param, torch.Tensor)  # pyright
            param_state = opt_state[param]
            new_state = {
                'param_dtype': param_state['param_dtype'],
                'master_weight_bytes': param_state['master_weight_bytes'],
            }
            if self._check_numerics:
                # can't read from old state since sharding might have changed;
                # also, value might be undefined with FSDP since it will
                # vary across ranks
                new_state['param_std'] = float(param.detach().std().float())
            for key_quant in self._quantized_state_keys():
                if any(k.startswith(key_quant) for k in param_state):
                    # the keys can either be just "exp_avg" or
                    # "exp_avg::quantized" and "exp_avg::scales", depending on
                    # whether we saved it as quantized or not. The former case
                    # gives us interop with regular LION.
                    qtensor = _MaybeQuantizedTensor(None,
                                                    try_quantize=self._quantize)
                    qtensor.load_state_dict(param_state, name=key_quant)
                    new_state[key_quant] = qtensor
            if 'errors' in param_state:  # just tries to fail fast
                new_state['error_dtype'] = param_state['error_dtype']
                new_state['numel'] = param.numel()  # sharding can change

                # throw if the parameter dtype somehow changed
                old_param_dtype = param_state['param_dtype']
                if param.dtype != old_param_dtype:
                    raise NotImplementedError(
                        'Cannot load error correction tensor from param with ' +
                        f'dtype {old_param_dtype} into param with dtype ' +
                        f'{param.dtype}')

                # throw if error width doesn't match master bitwidth
                param_bitwidth = _DTYPE_WIDTHS[param.dtype]
                need_err_bitwidth = self._master_weight_bits - param_bitwidth
                old_err_bitwidth = _DTYPE_WIDTHS[param_state['error_dtype']]
                if need_err_bitwidth != old_err_bitwidth:
                    raise NotImplementedError(
                        f'Cannot load {old_err_bitwidth}-bit error ' +
                        'correction tensor for parameter of dtype ' +
                        f'{param.dtype} when requested master weight ' +
                        f'bitwidth is {self._master_weight_bits}.')

                if need_err_bitwidth > 0:
                    errs = param_state['errors']
                    # add errors to state dict, undoing our Optimizer casting
                    # workaround and re-padding if needed
                    if need_err_bitwidth == 8 and param_bitwidth == 16:
                        errs = errs.to(dtype=torch.uint8)
                        errs.resize_(errs.numel() + (errs.numel() % 2))
                        errs = errs.view(dtype=param.dtype)
                    new_state['errors'] = errs

            opt_state[param] = new_state
        super().__setstate__(state)

    def state_dict(self):
        d = super().state_dict()
        opt_state, _ = d.values()  # other val is param_groups
        for param_id in opt_state:
            # make a copy so that we don't mutate our self.state; opt_state
            # isn't the same as self.state, but its consituent dicts are
            # the same as those in self.state
            param_state = {k: v for k, v in opt_state[param_id].items()}
            for key_quant in self._quantized_state_keys():
                if key_quant in param_state:  # true if we've taken any steps
                    # If the user hasn't opted into storing compressed state dicts
                    # we have to make sure our states are regular torch.Tensors.
                    # This is mostly needed to make FSDP happy in the case that
                    # we want to resume training with a number of devices where
                    #   (param numel / device count) % quantization group size != 0
                    # for any param.
                    qtensor = param_state.pop(key_quant)
                    assert isinstance(qtensor, _MaybeQuantizedTensor)  # pyright
                    param_state.update(
                        qtensor.state_dict(
                            name=key_quant,
                            allow_quantized=self._compress_state_dict))
            if 'errors' in param_state:
                # FSDP assumes that all non-scalar opt states have the
                # same shape as the params. Since Optimizer also casts these
                # states to the param dtype, we have to carefully change the
                # dtypes if the errors and params don't have the same bitwidth
                param_dtype = param_state['param_dtype']
                param_bytewidth = _DTYPE_WIDTHS[param_dtype] // 8
                master_bytewidth = self._master_weight_bits // 8
                error_width = master_bytewidth - param_bytewidth
                errs = param_state['errors']
                if error_width == 1 and param_bytewidth == 2:
                    errs = errs.view(dtype=torch.uint8)[:param_state['numel']]
                    # uint8 -> [b]f16 conversion is lossless, so this is safe
                    param_state['errors'] = errs.to(dtype=param_dtype)

                elif error_width == 2 and param_bytewidth == 1:
                    raise NotImplementedError(
                        'Cannot save 16-bit error correction tensor for 8-bit' +
                        'parameter. This is bacause FSDP requires that ' +
                        'non-scalar state variables have the same shape as ' +
                        'their param, while optim.Optimizer auto-casts state ' +
                        'tensors to the param dtype before calling ' +
                        'load_state_dict().' +
                        'It is not possible to work around both of these ' +
                        'behaviors simultaneously without information loss ' +
                        '(or far more implementation complexity).')

            opt_state[param_id] = param_state
        return d

    def _ensure_state_initialized(self, p: torch.Tensor,
                                  state: Dict[str, Any]) -> None:
        if 'param_dtype' not in state:
            state['param_dtype'] = p.dtype
        if 'master_weight_bytes' not in state:
            state['master_weight_bytes'] = self._master_weight_bits // 8
        if self._check_numerics:
            self.recompute_param_stats()  # sets param stds
        for key_quant in self._quantized_state_keys():
            if key_quant not in state:
                mom = torch.zeros_like(p)
                state[key_quant] = _MaybeQuantizedTensor(
                    mom, try_quantize=self._quantize)
        bitwidth = _DTYPE_WIDTHS[state['param_dtype']]
        num_err_bits = self._master_weight_bits - bitwidth

        if state.get('errors') is None and num_err_bits > 0:
            numel = p.numel()
            need_ecc_kernel = True
            if num_err_bits == 8:
                if bitwidth == 16:  # 32 doesn't need padding since no errs
                    numel += numel % 2
                err_dtype = torch.uint8
                errors = torch.zeros(numel, dtype=torch.uint8, device=p.device)
            elif num_err_bits == 16:  # 16 error correction bits
                errors = torch.zeros(numel, dtype=torch.int16, device=p.device)
                err_dtype = torch.int16
            else:  # just store full master weights instead of errors
                need_ecc_kernel = False
                errors = p.to(dtype=torch.float32)
                err_dtype = torch.float32

            state['numel'] = numel  # plumbing so state_dict() can unpad
            state['error_dtype'] = err_dtype

            if need_ecc_kernel and not self._fused:
                raise NotImplementedError(
                    f'Param of dtype {p.dtype} requires {num_err_bits} error ' +
                    f'correction bits to achieve requested master weight bit ' +
                    f'depth of {self._master_weight_bits}, but error ' +
                    'correction is only supported when quantize=True and ' +
                    '_fused=True.')

            # as of torch 2.1, FSDP can't shard ints for no reason; also,
            # viewing the errors as the same dtype as the param ensures that
            # load_state_dict's unavoidable casting to the param dtype is
            # a no-op
            state['errors'] = errors.view(p.dtype)

    def _check_param_numerics(self, p: torch.Tensor, lr: float) -> None:
        state = self.state[p]  # type:ignore using tensor as key
        param_bitwidth = _DTYPE_WIDTHS[p.dtype]
        std = max(state['param_std'], 2**-param_bitwidth)  # handle 0 std
        exponent = np.log2(std)
        bitwidth = max(self._master_weight_bits, param_bitwidth)
        log_min_expressible_step_size = exponent - bitwidth
        # 2 is a made up safety factor, since not all weights have the
        # same exponent
        if log_min_expressible_step_size > 2 + np.log2(lr):
            raise torch.linalg.LinAlgError(
                f'Learning rate {lr} yields steps that may be too small ' +
                f'to alter the weights for dtype {p.dtype} with master ' +
                f'weight minimum bit width {self._master_weight_bits}. ' +
                'Consider increasing your learning rate, decreasing your ' +
                'weight magnitudes, or increasing master_weight_bytes. ' +
                'Set check_numerics=False to disable this check. If ' +
                'you\'re getting this error after loading a checkpoint, ' +
                'you can call reset_param_stats() throughout training ' +
                'to fail faster and avoid this surprise.')

    @abc.abstractmethod
    def _do_step(self, param: torch.Tensor, grad: torch.Tensor,
                 errors: Optional[torch.Tensor], weight_decay: float,
                 state: Dict[str, Any], hparams: Dict[str, Any]) -> None:
        ...


class DecoupledLionW_8bit(_CompressedOptimizer):

    def _quantized_state_keys(self) -> Tuple[str, ...]:
        return ('exp_avg',)

    def _do_step(self, param: torch.Tensor, grad: torch.Tensor,
                 errors: Optional[torch.Tensor], weight_decay: float,
                 state: Dict[str, Any], hparams: Dict[str, Any]) -> None:
        _lion8b_step(momentums=state['exp_avg'],
                     weights=param,
                     grads=grad,
                     beta1=hparams['betas'][0],
                     beta2=hparams['betas'][1],
                     lr=hparams['lr'],
                     weight_decay=weight_decay,
                     fused=hparams['fused'],
                     errors=errors)


class _MaybeQuantizedTensor:
    """Helper class so 8b LION doesn't have to know quantization details.

    Important points about this class:
    * It handles CPU tensors not being quantized
    * It knows how to save + load state dicts, handling both the quantized
        and not quantized cases
    * It implements some parts of the torch.Tensor interface that we need,
        but is not intended to be a full torch.Tensor replacement
    """

    def __init__(self, data: Optional[torch.Tensor], try_quantize: bool = True):
        super().__init__()
        self.data: Optional[torch.Tensor] = None
        self.quantized: Optional[torch.Tensor] = None
        self.scales: Optional[torch.Tensor] = None
        self._try_quantize = try_quantize and torch.cuda.is_available()

        # conditionally import CUDA kernels
        self._f_encode = None
        self._f_decode = None
        if self._try_quantize:
            from turbo import dequantize_signed, quantize_signed
            self._f_encode = quantize_signed
            self._f_decode = dequantize_signed

        if data is not None:
            self.set_data(data)

    def state_dict(self,
                   name: str,
                   allow_quantized: bool = False) -> Dict[str, torch.Tensor]:
        if self.is_quantized() and allow_quantized:
            assert self.quantized is not None  # pyright
            assert self.scales is not None  # pyright
            return {
                f'{name}::quantized': self.quantized,
                f'{name}::scales': self.scales
            }
        return {name: self.materialize().to(dtype=torch.bfloat16)}

    def load_state_dict(self, d: Dict[str, torch.Tensor], name: str) -> None:
        # we allow other keys in the state dict for convenience, so you can
        # just pass this the whole opt state for a parameters
        d = {k: v for k, v in d.items() if k.startswith(name)}
        if name in d:
            if len(d) != 1:
                raise ValueError(
                    f'If state dict specifies {name}, it must not ' +
                    f'specify other keys. Got {list(d.keys())}')
            self.set_data(d[name])
            return

        self.quantized = d[f'{name}::quantized'].to(dtype=torch.int8)
        self.scales = d[f'{name}::scales'].to(dtype=torch.float16)

    def set_data(self, data: torch.Tensor) -> None:
        if self._try_quantize:
            if not data.is_cuda:
                raise NotImplementedError(
                    f'Attempting to quantize a non-CUDA {data.dtype} tensor ' +
                    f'on device {data.device} with shape {data.shape}.')
            self.data = None
            assert self._f_encode is not None  # pyright
            self.quantized, self.scales, _ = self._f_encode(data)
        else:
            self.data = data.to(dtype=torch.float32)
            self.quantized = None
            self.scales = None

    def is_quantized(self) -> bool:
        return self.data is None

    def materialize(self) -> torch.Tensor:
        if not self.is_quantized():
            assert self.data is not None  # pyright
            return self.data
        assert self._f_decode is not None  # pyright
        assert self.quantized is not None  # pyright
        assert self.scales is not None  # pyright
        return self._f_decode(self.quantized, self.scales)

    @property  # property to mirror Tensor interface
    def is_cuda(self) -> bool:
        if self.is_quantized():
            assert self.quantized is not None  # pyright
            return self.quantized.is_cuda
        assert self.data is not None  # pyright
        return self.data.is_cuda

    @property  # property to mirror Tensor interface
    def shape(self) -> Tuple[int, ...]:
        if self.is_quantized():
            assert self.quantized is not None  # pyright
            return tuple(self.quantized.shape)
        assert self.data is not None  # pyright
        return tuple(self.data.shape)

    def numel(self) -> int:
        if self.is_quantized():
            assert self.quantized is not None  # pyright
            return self.quantized.numel()
        assert self.data is not None  # pyright
        return self.data.numel()

    def __repr__(self):
        return (f'{self.__class__.__name__} quantized={self.is_quantized()} ' +
                f'shape={self.shape}')


def lion_step_unfused(grads: torch.Tensor,
                      weights: torch.Tensor,
                      momentums: torch.Tensor,
                      lr: float,
                      beta1: float,
                      beta2: float,
                      weight_decay: float = 0) -> torch.Tensor:
    # f32 cast to match fused impl + for compatibility with f32 grads or weights
    momentums = momentums.to(dtype=torch.float32)
    grads = grads.to(dtype=torch.float32)

    update = momentums.lerp(grads, 1 - beta1).sign_()
    if weight_decay > 0:
        weights.mul_(1. - weight_decay)

    weights.add_(update, alpha=-lr)
    momentums.lerp_(grads, 1. - beta2)
    return momentums  # f32 upcast means not necessarily modified in place


def lion8b_step_fused(grads: torch.Tensor,
                      weights: torch.Tensor,
                      momentums: torch.Tensor,
                      scales: torch.Tensor,
                      lr: float,
                      beta1: float,
                      beta2: float,
                      weight_decay: float,
                      errors: Optional[torch.Tensor] = None) -> None:
    # just to save space in lists of allowed dtypes
    f16, bf16, f32 = torch.float16, torch.bfloat16, torch.float32

    use_errors = (errors is not None) and (weights.dtype in (f16, bf16))
    if use_errors:
        assert errors is not None  # pyright
        if errors.dtype not in [torch.uint8, torch.int16]:
            raise ValueError("expected errors to have type uint8 or int16")
    orig_shape = weights.shape

    # ------------------------------------------------ wall of error checking
    quantize_group_size = 32
    num_groups = (weights.numel() + quantize_group_size -
                  1) // quantize_group_size
    if (num_groups != scales.numel()):
        raise ValueError(f'Expected {num_groups} quantization scales but ' +
                         f' received {scales.numel()}')

    for name, tensor, allowed_dtypes in [('grad', grads, (f16, bf16, f32)),
                                         ('param', weights, (f16, bf16, f32)),
                                         ('momentum', momentums, [torch.int8]),
                                         ('scales', scales, [f16]),
                                         ('errors', errors,
                                          [torch.uint8, torch.int16])]:
        if name == 'errors' and not use_errors:
            continue
        if not tensor.is_cuda:
            raise ValueError(
                f'{name} must be on a CUDA device, not {tensor.device}')
        if not tensor.is_contiguous():
            raise ValueError(f'{name} is not contiguous!')
        strides_unequal = tensor.stride() != weights.stride()
        if name not in ('scales', 'errors') and strides_unequal:
            raise ValueError(f'{name} stride {tensor.stride()} != ' +
                             f'param stride {weights.stride()}')
        if tensor.dtype not in allowed_dtypes:
            raise ValueError(f'{name} must have dtype {allowed_dtypes}, not ' +
                             f'{tensor.dtype}')
        if (name != 'scales') and (orig_shape != tensor.shape):
            raise ValueError(f'Param shape {orig_shape} != ' +
                             f'{name} shape {tensor.shape}')

    if grads.dtype in (torch.float16, torch.bfloat16):
        allowed_dtypes = (grads.dtype, torch.float32)
        if weights.dtype not in allowed_dtypes:
            raise ValueError(
                f'Weights must be f32 or match grad dtype {grads.dtype}')

    # ------------------------------------------------ actual function call
    from turbo import lion8b_step_cuda
    return lion8b_step_cuda(grads=grads,
                            weights=weights,
                            momentums=momentums,
                            scales=scales,
                            lr=lr,
                            beta1=beta1,
                            beta2=beta2,
                            weight_decay=weight_decay,
                            errors=errors)


def _lion8b_step(grads: torch.Tensor,
                 weights: torch.Tensor,
                 momentums: _MaybeQuantizedTensor,
                 lr: float,
                 beta1: float,
                 beta2: float,
                 weight_decay: float = 0,
                 errors: Optional[torch.Tensor] = None,
                 fused: bool = True) -> None:

    if fused and not momentums.is_quantized():
        raise NotImplementedError(
            'Fused LION step only implemented with quantization.')
    if errors is not None:
        if errors.dtype not in [torch.uint8, torch.int16]:
            raise ValueError("Errors needs to be uint8 or int16")
    if momentums.is_quantized() and fused:
        assert momentums.quantized is not None  # pyright
        assert momentums.scales is not None  # pyright
        return lion8b_step_fused(grads=grads,
                                 weights=weights,
                                 momentums=momentums.quantized,
                                 scales=momentums.scales,
                                 lr=lr,
                                 beta1=beta1,
                                 beta2=beta2,
                                 weight_decay=weight_decay,
                                 errors=errors)

    momentums_float = momentums.materialize()
    new_momentums = lion_step_unfused(grads=grads,
                                      weights=weights,
                                      momentums=momentums_float,
                                      lr=lr,
                                      beta1=beta1,
                                      beta2=beta2,
                                      weight_decay=weight_decay)
    momentums.set_data(new_momentums)
