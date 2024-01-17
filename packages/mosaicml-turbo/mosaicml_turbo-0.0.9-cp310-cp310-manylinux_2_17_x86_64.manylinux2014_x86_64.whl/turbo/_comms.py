import dataclasses
import functools
from typing import Callable, Optional, Protocol

import torch
from torch._C._distributed_c10d import AllgatherOptions  # type: ignore
from torch.distributed import ProcessGroup, Work, get_world_size  # type: ignore

from . import _codecs as codecs
from ._codecs import Codec

_DEFAULT_MIN_MESSAGE_SIZE = 1 << 15  # 32kiB
_g_min_message_bytes_to_compress = _DEFAULT_MIN_MESSAGE_SIZE


class Waitable(Protocol):
    """An object you can call wait() on.

    Meaning varies. Mostly for typing.
    """

    def wait(self) -> None:
        ...


@dataclasses.dataclass
class SimpleFuture:
    callback: Callable

    def wait(self) -> None:
        self.callback()


# ================================================================ codecs


# TODO rm this function once we're done testing different codecs
def _fp8_compressed_allgather_codec() -> Codec:  # type: ignore
    return codecs.CastCodec(dtype=torch.float8_e5m2)  # type: ignore


def _int8_compressed_allgather_codec() -> Codec:
    # we can get away with not clipping because FSDP pads with ones, not empty()
    # see:
    # -https://github.com/pytorch/pytorch/blob/7d61fa23df4f3608876461b98043d7ef4fd96978/torch/distributed/fsdp/_flat_param.py#L673 # noqa
    # -https://github.com/pytorch/pytorch/blob/7d61fa23df4f3608876461b98043d7ef4fd96978/torch/distributed/fsdp/_flat_param.py#L2683 # noqa
    return codecs.SignedIntQuantizer(num_bits=8)


def _clipped_int8_codec(  # type: ignore
        clip_min: float = -4, clip_max: float = 4) -> Codec:
    f_nan2num = functools.partial(torch.nan_to_num, neginf=0, posinf=0)
    f_clip = functools.partial(torch.clip, min=clip_min, max=clip_max)
    assert isinstance(f_nan2num, codecs.LambdaCodec.CodecFunction)  # pyright
    assert isinstance(f_clip, codecs.LambdaCodec.CodecFunction)  # pyright
    return codecs.SequentialCodec([
        codecs.LambdaCodec(f_nan2num),
        codecs.LambdaCodec(f_clip),
        _int8_compressed_allgather_codec(),
    ])


def _default_compressed_allgather_codec() -> Codec:
    return _int8_compressed_allgather_codec()
    # return _fp8_compressed_allgather_codec()


# ================================================================ ProcessGroup

# TODO this state machine is a bit confusing. Maybe just expose the
# whitelist directly to avoid leaky abstractions.
_g_patched_allgather_procgroups = set()
_g_raw_allgather_base = ProcessGroup._allgather_base


def _undo_monkey_patches():
    ProcessGroup._allgather_base = _g_raw_allgather_base  # type: ignore


def set_min_message_size_to_compress(num_bytes: int) -> None:
    global _g_min_message_bytes_to_compress
    _g_min_message_bytes_to_compress = num_bytes


def disable_compressed_allgathers(pg: Optional[ProcessGroup] = None) -> None:
    """Replaces compressed allgathers with unmodified ones.

    See ~`.enable_compressed_allgathers` for more details.

    Args:
        pg: If `None`, compressed allgathers are disabled for all process
            groups and the whitelist is cleared. If not `None`, `pg`
            is just removed from the whitelist.

    Raises:
        ValueError: If `pg` is not in the whitelist of process groups
            with allgather compression enabled.
    """
    global _allgathers_globally_enabled
    if pg is None:
        _g_patched_allgather_procgroups.clear()
        _undo_monkey_patches()
        return
    if pg not in _g_patched_allgather_procgroups:
        raise ValueError(f'ProcessGroup {pg} not found in whitelist: ' +
                         f'{list(_g_patched_allgather_procgroups)}')
    _g_patched_allgather_procgroups.remove(pg)
    # don't accidentally turn on compression for *all* pgs by
    # removing the last element of the whitelist
    if not len(_g_patched_allgather_procgroups):
        _undo_monkey_patches()


def enable_compressed_allgathers(pg: Optional[ProcessGroup] = None,
                                 codec: Optional[Codec] = None,
                                 pg_world_size: Optional[int] = None) -> None:
    """Turns on 8-bit compression for allgather operations.

    Because this function requires us to monkey patch the `ProcessGroup`
    itself (not particular instances), the function works as follows:

    * When you first call this function, `ProcessGroup` gets monkey patched
    * If given a `ProcessGroup`, that group is added to a whitelist.
    * If there is a non-empty whitelist, ProcessGroup instances not in
        the whitelist will use regular, non-compressed allgathers.

    The subltety here is that, if there was a non-empty whitelist and you
    remove the last group from it via `disable_compressed_allgathers`,
    allgathers remain globally disabled until you call
    `enable_compressed_allgathers` again. This is so that going from a
    non-empty whitelist to an empty one doesn't suddenly turn on compressed
    allgathers for all `ProcessGroup`s.

    Args:
        pg: A `ProcessGroup` whose allgathers should be compressed. If `None`,
            all `ProcessGroup`s' allgathers will be compressed.
        codec: A `turbo._codecs.Codec` to run on the allgather inputs and
            each shard of the allgather outputs. If `None`, allgathers will
            use a default Codec that performs chunked 8-bit quantization.
        pg_world_size: The world size of the process groups to enable
            compression for. If `None`, all process groups have compressed
            all gathers.
    """
    if codec is None:
        codec = _default_compressed_allgather_codec()

    global _g_patched_allgather_procgroups
    if pg is not None:
        _g_patched_allgather_procgroups.add(pg)

    @functools.wraps(ProcessGroup._allgather_base)
    def _allgather_base(pg_self: ProcessGroup,
                        out_tensor: torch.Tensor,
                        in_tensor: torch.Tensor,
                        opts: Optional[AllgatherOptions] = None,
                        _codec: Codec = codec):
        opts = opts or AllgatherOptions()

        # just behave normally if this isn't a group we wanted to patch
        whitelisted = pg_self in _g_patched_allgather_procgroups
        whitelisted = whitelisted or not len(_g_patched_allgather_procgroups)
        supported_dtypes = {torch.float16, torch.bfloat16, torch.float32}
        valid_dtype = (in_tensor.dtype in supported_dtypes and
                       out_tensor.dtype in supported_dtypes)
        global _g_min_message_bytes_to_compress
        in_bytes = in_tensor.numel() * in_tensor.element_size()
        too_small = in_bytes < _g_min_message_bytes_to_compress
        incorrect_world_size = (pg_world_size
                                is not None) and (get_world_size(pg_self)
                                                  != pg_world_size)
        if (not whitelisted) or (
                not valid_dtype) or too_small or incorrect_world_size:
            return _g_raw_allgather_base(pg_self, out_tensor, in_tensor, opts)

        in_compressed = _codec.encode(in_tensor)
        num_ranks = out_tensor.numel() // in_tensor.numel()
        out_compressed_numel = num_ranks * in_compressed.numel()
        out_compressed = torch.empty(out_compressed_numel,
                                     dtype=in_compressed.dtype,
                                     device=in_compressed.device)

        # allgather_into_tensor still calls pg's _allgather_base:
        # https://github.com/pytorch/pytorch/blob/362bc6d7cbcac57466a52701fac3ba3bfb668000/torch/distributed/distributed_c10d.py#L2811 # noqa
        # the python functional wrapper returns Optional[Work], but the pg
        # itself always returns work
        handle: Work = _g_raw_allgather_base(pg_self, out_compressed,
                                             in_compressed, opts)

        # decompression callback to run after the async call waits
        def _copy_into_output(_out_compressed: torch.Tensor = out_compressed,
                              _out_raw: torch.Tensor = out_tensor,
                              _num_chunks: int = num_ranks,
                              __codec: Codec = _codec,
                              _handle: Work = handle) -> None:
            _handle.wait()
            __codec.decode(_out_compressed,
                           batch_size=_num_chunks,
                           out=_out_raw)

        if getattr(opts, 'asyncOp', False):  # not an option until torch 2.2
            return SimpleFuture(callback=_copy_into_output)
        _copy_into_output()
        return handle

    ProcessGroup._allgather_base = _allgather_base  # type: ignore
