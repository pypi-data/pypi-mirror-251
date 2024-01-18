
import time
import tqdm
from datetime import timedelta
from typing import Callable, Any

def benchmark(*, name: str, cumulative: bool = False, range_start: int = 0, range_end: int = None) -> Callable:
    """
    Decorator function for benchmarking other functions.

    :param name: The name of the benchmark.
    :type name: str
    :param cumulative: Whether to benchmark a function a number of times with different inputs. If the decorated function returns a result, the sum of the total results is displayed. Defaults to False.
    :type cumulative: bool, optionals
    :param range_start: The start value of the range for cumulative benchmarking. Defaults to 0.
    :type range_start: int, optional
    :param range_end: The end value of the range for cumulative benchmarking. Defaults to the decorated function's first argument.
    :type range_end: int, optional
    :return: The decorated function.
    :rtype: function
    """
    def _with_config(fn: Callable[..., Any]) -> Callable[..., Any]:
        def _timed(*n: Any) -> Any:
            nonlocal range_end

            before = time.perf_counter()

            if cumulative:
                if len(n) == 0:
                    raise ValueError("Cumulative benchmarking requires the decorated function to receive at least one argument.")
                if not range_end:
                    range_end = n[0]
                res = sum(fn(i, *n[1:]) for i in tqdm.trange(range_start, range_end, desc=name, leave=False))
            else:
                res = fn(*n)

            after = time.perf_counter()

            diff = timedelta(seconds=after - before)

            print(
                f"{name}",
                f"{'Time':>12}: {diff}",
                f"{'Result':>12}: {res}\n" if res else "",
                sep="\n",
            )

        return _timed

    return _with_config
