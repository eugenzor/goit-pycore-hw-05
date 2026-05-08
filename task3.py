import sys
from collections import Counter
from pathlib import Path

from rich.console import Console
from rich.table import Table


KNOWN_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> dict:
    """Розібрати рядок логу на дату, час, рівень та повідомлення."""
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        return {}
    date, time, level, message = parts
    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
    }


def load_logs(file_path: str) -> list:
    """Завантажити та розпарсити логи з файлу."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as fh:
        return [parsed for line in fh if (parsed := parse_log_line(line))]


def filter_logs_by_level(logs: list, level: str) -> list:
    """Відфільтрувати записи логу за вказаним рівнем."""
    target = level.upper()
    return list(filter(lambda log: log.get("level") == target, logs))


def count_logs_by_level(logs: list) -> dict:
    """Підрахувати кількість записів для кожного рівня логування."""
    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict) -> None:
    """Вивести підсумкову таблицю кількості записів за рівнями."""
    console = Console()
    table = Table(title="Статистика логів за рівнями")
    table.add_column("Рівень логування", style="cyan", no_wrap=True)
    table.add_column("Кількість", justify="right", style="magenta")

    levels = list(KNOWN_LEVELS) + [lvl for lvl in counts if lvl not in KNOWN_LEVELS]
    for level in levels:
        if level in counts:
            table.add_row(level, str(counts[level]))

    console.print(table)


def display_log_details(logs: list, level: str) -> None:
    """Вивести детальну інформацію про записи певного рівня."""
    console = Console()
    filtered = filter_logs_by_level(logs, level)

    if not filtered:
        console.print(f"[yellow]Записів рівня '{level.upper()}' не знайдено.[/yellow]")
        return

    console.print(f"\n[bold]Деталі логів для рівня '{level.upper()}':[/bold]")
    for log in filtered:
        console.print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    console = Console()

    if len(sys.argv) < 2:
        console.print("[red]Usage: python task3.py <log_file> [level][/red]")
        sys.exit(1)

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        console.print(f"[red]Файл '{file_path}' не знайдено.[/red]")
        sys.exit(1)
    except OSError as exc:
        console.print(f"[red]Помилка читання файлу: {exc}[/red]")
        sys.exit(1)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level:
        display_log_details(logs, level)


if __name__ == "__main__":
    main()
