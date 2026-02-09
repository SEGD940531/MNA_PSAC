from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


HEX_DIGITS = "0123456789ABCDEF"


@dataclass(frozen=True)
class ConversionResult:
    """Represents a successful conversion for an integer input."""
    decimal: int
    binary: str
    hexadecimal: str


def parse_int_strict(text: str) -> Optional[int]:
    """
    Parse an integer from a string strictly.
    Returns None if invalid.

    Notes:
    - Accepts leading/trailing spaces.
    - Accepts optional '+' or '-' sign.
    - Rejects floats/scientific notation and empty strings.
    """
    raw = text.strip()
    if raw == "":
        return None

    sign = 1
    if raw[0] in ("+", "-"):
        if raw[0] == "-":
            sign = -1
        raw = raw[1:]

    if raw == "":
        return None

    # Validate all characters are digits (basic algorithm constraint)
    for ch in raw:
        if ch < "0" or ch > "9":
            return None

    value = 0
    for ch in raw:
        digit = ord(ch) - ord("0")
        value = value * 10 + digit

    return sign * value


def _convert_positive_to_base(n: int, base: int) -> str:
    """
    Convert a non-negative integer to a base using repeated division.
    This is a basic algorithm (no bin/hex helpers).
    """
    if n == 0:
        return "0"

    digits: list[str] = []
    current = n
    while current > 0:
        remainder = current % base
        if base == 16:
            digits.append(HEX_DIGITS[remainder])
        else:
            digits.append(str(remainder))
        current //= base

    # Reverse digits
    return "".join(reversed(digits))


def to_binary(n: int) -> str:
    """Convert integer to binary string using basic algorithm."""
    if n < 0:
        return "-" + _convert_positive_to_base(-n, 2)
    return _convert_positive_to_base(n, 2)


def to_hexadecimal(n: int) -> str:
    """Convert integer to hexadecimal string using basic algorithm."""
    if n < 0:
        return "-" + _convert_positive_to_base(-n, 16)
    return _convert_positive_to_base(n, 16)


def convert_number(n: int) -> ConversionResult:
    """Convert integer to binary and hexadecimal representations."""
    return ConversionResult(
        decimal=n,
        binary=to_binary(n),
        hexadecimal=to_hexadecimal(n),
    )