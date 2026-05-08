import re
from typing import Callable, Generator

from rich.console import Console
from rich.table import Table


NUMBER_PATTERN = re.compile(r"(?<=\s)\d+(?:\.\d+)?(?=\s)")


def generator_numbers(text: str) -> Generator[float, None, None]:
    """Генерувати дійсні числа з тексту, відокремлені пробілами з обох боків."""
    for match in NUMBER_PATTERN.finditer(text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """Просумувати усі числа, що повертає переданий генератор."""
    return sum(func(text))


def main() -> None:
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )

    numbers = list(generator_numbers(text))
    total_income = sum_profit(text, generator_numbers)

    console = Console()

    table = Table(title="Знайдені числа в тексті")
    table.add_column("№", justify="right", style="cyan")
    table.add_column("Значення", justify="right", style="magenta")
    for index, value in enumerate(numbers, start=1):
        table.add_row(str(index), f"{value:.2f}")

    console.print(table)
    console.print(f"[bold green]Загальний дохід:[/bold green] {total_income}")


if __name__ == "__main__":
    main()
