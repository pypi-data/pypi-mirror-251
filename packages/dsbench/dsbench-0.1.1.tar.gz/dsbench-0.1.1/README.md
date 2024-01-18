# DSBench

This small library provides a decorator function that benchmarks functions.

### dsbench.benchmark(\*, name: str, cumulative: bool = False, range_start: int = 0, range_end: int = None) -> Callable

Decorator function for benchmarking other functions.

* **Parameters:**
  * **name** (*str*) – The name of the benchmark.
  * **cumulative** (*bool* *,* *optionals*) – Whether to benchmark a function a number of times with different inputs. If the decorated function returns a result, the sum of the total results is displayed. Defaults to False.
  * **range_start** (*int* *,* *optional*) – The start value of the range for cumulative benchmarking. Defaults to 0.
  * **range_end** (*int* *,* *optional*) – The end value of the range for cumulative benchmarking. Defaults to the decorated function’s first argument.
* **Returns:**
  The decorated function.
* **Return type:**
  function
