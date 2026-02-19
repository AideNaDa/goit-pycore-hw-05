from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """
    Return a Fibonacci function with caching.
    """
    cache = {}

    def fibonacci(n: int) -> int:
        """
        Calculate Fibonacci number using cache.
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
