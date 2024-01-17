import itertools
import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence

import pandas as pd
import torch
import torch.distributed as dist


def _dicts_to_dataframe(d: Sequence[Dict[Any, Any]]) -> pd.DataFrame:
    """Convert a dict or collection of dicts to a Pandas DataFrame.

    This is just a wrapper around `pd.DataFrame.from_records` that handles
    individual dicts being passed in along with different types of indexes.
    """
    if not isinstance(d, dict):
        try:
            df = pd.DataFrame.from_records(d)
        except Exception:
            dfs = [pd.DataFrame.from_records(dd, index=[0]) for dd in d]
            df = pd.concat(dfs, axis=0, ignore_index=True)
    else:
        df = pd.DataFrame.from_records(d, index=[0])
    return df


def _generate_valid_combos(params: Dict[str, Any],
                           f_valid: Optional[Callable[[Dict[str, Any]],
                                                      bool]] = None):
    """Generates (valid subset of) Cartesian product of different parameters.

    This function essentially just lifts `itertools.product` to operate on
    dicts and skips parameter combinations for which some predicate is false.

    Args:
        params: A dictionary of param name: value. If value is a collection,
            the elements will be passed in individually / the collection will
            be treated as a set of values to sweep over. To pass in an entire
            collection without sweeping over it, wrap it in a `list` or other
            iterable.
        f_valid: If provided, each parameter combination is passed to this
            function before being yielded. If this function returns false,
            the dictionary is not yielded.

    Returns:
        Yields each valid combination of parameters from the Cartesian product
        over all entries as a dict.
    """
    keys = list(params.keys())
    values = [params[k] for k in keys]

    def _is_sequence(val: Any) -> bool:
        return isinstance(val, Sequence) and not isinstance(val, str)

    # wrap non-collection elements in singleton lists so itertools.product
    # doesn't choke on them
    values = [(val if _is_sequence(val) else [val]) for val in values]
    for values_combo in itertools.product(*values):
        combo = {keys[i]: values_combo[i] for i in range(len(keys))}
        if (f_valid is not None) and (not f_valid(combo)):
            continue
        yield combo


def run_experiment(
    f_run: Callable[[Any], Dict],
    params_grid: Optional[Dict[str, Any]] = None,
    params_generator: Optional[Iterable] = None,
    f_params_valid: Optional[Callable[[Dict[str, Any]], bool]] = None,
) -> pd.DataFrame:
    """Call a function on many sets of args and return a dataframe of results.

    Each row contains the parameters passed to the function and whatever
    keys and values are present in the dictionary it returns.

    Args:
        f_run: Callable that takes in arguments from either `params_grid` or
            `params_generator` and returns a dictionary. The returned
            dictionary can have arbitrary keys and values. Optionally,
            `f_run` can also implement a method `params()` that returns an
            additional dictionary to be stored along with its results.
        params_grid: A dictionary optionally containing one or more
            collections. The Cartesian product of
            all values in all collections is fed one at a time into `f_run` as
            keyword arguments (along with the keys and values) of the
            non-collection elements of `params_grid`. Callers must specify
            either `params_grid` or `params_generator`, but not both.
        params_generator: An iterable whose elements are dictionaries of
            parameters to be passed to `f_run` as keyword arguments. Callers
            must specify either `params_grid` or `params_generator`, but
            not both.
        f_params_valid: A function to test whether a given set of parameters
            should actually be passed to `f_run` (if it returns `True`) or
            discarded (if it returns `False`). This is useful when only
            certain combinations of parameters make sense, or when some
            parameters do not affect the result conditioned on other parameters
            having certain values---e.g., a regularization parameter that does
            not apply to one algorithm being tested.

    Returns:
        The DataFrame of parameters and results aggregated across all calls
        to `f_run`.
    """
    if (params_generator is not None) and (params_grid is not None):
        raise ValueError('Must supply either params_grid or params_generator,' +
                         ' but not both!')

    # create generator for parameter combos
    if params_generator is None:
        if params_grid is None or len(params_grid) == 0:
            # we can't put this in the generator function because yield
            # and return don't play nicely together in one function
            params_generator = [{}]
        else:
            params_generator = _generate_valid_combos(params_grid,
                                                      f_valid=f_params_valid)

    # run function on parameter combos and capture both results and params
    all_results = []
    for params in params_generator:
        results = (
            f_run() if len(params) == 0  # type: ignore
            else f_run(**params))  # type: ignore
        if not isinstance(results, list):  # handle single result per func call
            results = [results]
        for result in results:
            for k, v in params.items():
                result.setdefault(k, v)
            all_results.append(result)
    return _dicts_to_dataframe(all_results)


def _make_barrier_func():
    have_cuda = torch.cuda.is_available()
    distributed = dist.get_world_size() > 1
    if have_cuda:
        if distributed:
            return lambda: torch.cuda.synchronize()
            dist.barrier()
        else:
            return lambda: torch.cuda.synchronize()
    else:
        if distributed:
            return lambda: dist.barrier()
        else:
            return lambda: None


def time_func(f_run: Callable,
              f_setup: Optional[Callable] = None,
              num_trials: int = 5,
              num_iters: int = 1,
              num_warmup_iters: int = 4,
              verbose: bool = False) -> List[float]:
    if f_setup is None:
        f_setup = lambda: None  # noqa: E731
    f_barrier = _make_barrier_func()
    times = []
    for t in range(num_warmup_iters):
        f_setup()
        f_run()
        if verbose:
            print(f"finished warmup iter {t + 1}/{num_warmup_iters}")
    f_barrier()
    for t in range(num_trials):
        f_setup()
        f_barrier()
        start = time.time()
        for _ in range(num_iters):
            f_run()
        f_barrier()
        t_microsecs = (time.time() - start) / num_iters * 1e6
        times.append(t_microsecs)
        if verbose:
            print(f"finished trial {t + 1}/{num_trials}")
    return times
