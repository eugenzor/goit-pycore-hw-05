from functools import wraps
from typing import Callable

from rich.console import Console
from rich.table import Table


console = Console()


def input_error(func: Callable) -> Callable:
    """Декоратор, що перетворює типові винятки введення на повідомлення для користувача."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"

    return inner


def parse_input(user_input: str) -> tuple[str, ...]:
    """Розібрати рядок вводу на команду та аргументи."""
    if not user_input.strip():
        return ("",)
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    name = args[0]
    return contacts[name]


@input_error
def show_all(contacts: dict[str, str]):
    if not contacts:
        return "Contacts list is empty."

    table = Table(title="Contacts")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Phone", style="magenta")
    for name, phone in contacts.items():
        table.add_row(name, phone)

    return table


ASSISTANT_STYLE = "bold green"

COMMANDS = [
    ("hello", "", "Привітання від бота"),
    ("add", "<name> <phone>", "Додати новий контакт"),
    ("change", "<name> <phone>", "Оновити телефон існуючого контакту"),
    ("phone", "<name>", "Показати телефон контакту"),
    ("all", "", "Показати всі контакти"),
    ("close | exit", "", "Завершити роботу"),
]


def say(message) -> None:
    """Вивести повідомлення асистента: текст — стилізовано, renderable (наприклад Table) — як є."""
    if isinstance(message, str):
        console.print(message, style=ASSISTANT_STYLE)
    else:
        console.print(message)


def build_help() -> Table:
    """Зібрати таблицю-довідку зі списком команд."""
    table = Table(title="Available commands", title_style="bold yellow")
    table.add_column("Command", style="bold cyan", no_wrap=True)
    table.add_column("Arguments", style="magenta")
    table.add_column("Description", style="green")
    for command, arguments, description in COMMANDS:
        table.add_row(command, arguments, description)
    return table


def main() -> None:
    contacts: dict[str, str] = {}
    say("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                say("Good bye!")
                break
            case "hello":
                say("How can I help you?")
            case "add":
                say(add_contact(args, contacts))
            case "change":
                say(change_contact(args, contacts))
            case "phone":
                say(show_phone(args, contacts))
            case "all":
                say(show_all(contacts))
            case _:
                say("Invalid command.")
                say(build_help())


if __name__ == "__main__":
    main()
