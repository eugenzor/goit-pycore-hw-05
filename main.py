import sys
from pathlib import Path

import task1
import task2
import task3
import task4


TASK3_LOG_FILE = str(Path(__file__).parent / "files" / "example.log")
TASK3_LEVEL = "ERROR"


def run_section(title: str, runner) -> None:
    print(f"\n=== {title} ===")
    runner()


def run_task3() -> None:
    original_argv = sys.argv
    sys.argv = ["task3.py", TASK3_LOG_FILE, TASK3_LEVEL]
    try:
        task3.main()
    finally:
        sys.argv = original_argv


def main() -> None:
    run_section("Task 1: caching_fibonacci", task1.main)
    run_section("Task 2: generator_numbers / sum_profit", task2.main)
    run_section(
        f"Task 3: log analyzer (file='{TASK3_LOG_FILE}', level='{TASK3_LEVEL}')",
        run_task3,
    )
    run_section("Task 4: assistant bot with input_error", task4.main)


if __name__ == "__main__":
    main()
