from converter_core import (
    parse_int_strict,
    to_binary,
    to_hexadecimal,
    convert_number,
)


def test_parse_int_strict_valid() -> None:
    assert parse_int_strict("10") == 10
    assert parse_int_strict("   10  ") == 10
    assert parse_int_strict("+7") == 7
    assert parse_int_strict("-7") == -7
    assert parse_int_strict("0") == 0


def test_parse_int_strict_invalid() -> None:
    assert parse_int_strict("") is None
    assert parse_int_strict("   ") is None
    assert parse_int_strict("12.5") is None
    assert parse_int_strict("1e3") is None
    assert parse_int_strict("abc") is None
    assert parse_int_strict("--1") is None


def test_to_binary_basic() -> None:
    assert to_binary(0) == "0"
    assert to_binary(1) == "1"
    assert to_binary(2) == "10"
    assert to_binary(10) == "1010"
    assert to_binary(-10) == "-1010"


def test_to_hexadecimal_basic() -> None:
    assert to_hexadecimal(0) == "0"
    assert to_hexadecimal(10) == "A"
    assert to_hexadecimal(15) == "F"
    assert to_hexadecimal(16) == "10"
    assert to_hexadecimal(255) == "FF"
    assert to_hexadecimal(-255) == "-FF"


def test_convert_number() -> None:
    conv = convert_number(31)
    assert conv.decimal == 31
    assert conv.binary == "11111"
    assert conv.hexadecimal == "1F"