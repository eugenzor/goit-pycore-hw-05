from typing import Callable

from rich.console import Console
from rich.table import Table


def caching_fibonacci() -> Callable[[int], int]:
    """Створити функцію fibonacci(n) із кешем чисел Фібоначчі через замикання."""
    cache: dict[int, int] = {}

    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


def main() -> None:
    fib = caching_fibonacci()

    samples = [0, 1, 5, 10, 15, 20, 30]

    console = Console()
    table = Table(title="Числа Фібоначчі (з кешуванням)")
    table.add_column("n", justify="right", style="cyan", no_wrap=True)
    table.add_column("fib(n)", justify="right", style="magenta")

    for n in samples:
        table.add_row(str(n), str(fib(n)))

    console.print(table)


if __name__ == "__main__":
    main()
