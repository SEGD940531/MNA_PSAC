import logging
from typing import List


def read_numbers(path: str) -> List[float]:
    numbers: List[float] = []

    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                numbers.append(float(line))
            except ValueError:
                logging.error(
                    "Invalid value '%s' at line %s", line, line_number
                )

    return numbers
