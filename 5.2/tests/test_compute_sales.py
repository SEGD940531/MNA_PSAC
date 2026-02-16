import json

import pytest
from compute_sales import compute_sales


def _load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_expected_totals(path: str) -> dict:
    expected = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.upper() == "TOTAL":
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            tc, total = parts[0], parts[1]
            expected[tc] = total
    return expected


EXPECTED = _load_expected_totals("tests/expected/Results.txt")

CASES = [
    (
        "TC1",
        "tests/fixtures/valid/TC1/TC1.ProductList.json",
        "tests/fixtures/valid/TC1/TC1.Sales.json",
    ),
    (
        "TC2",
        "tests/fixtures/valid/TC1/TC1.ProductList.json",
        "tests/fixtures/valid/TC2/TC2.Sales.json",
    ),
    (
        "TC3",
        "tests/fixtures/valid/TC1/TC1.ProductList.json",
        "tests/fixtures/valid/TC3/TC3.Sales.json",
    ),
]


@pytest.mark.parametrize("tc_name,prices_path,sales_path", CASES, ids=[c[0] for c in CASES])
def test_tc_totals_match_expected(tc_name: str, prices_path: str, sales_path: str):
    prices = _load_json(prices_path)
    sales = _load_json(sales_path)

    result = compute_sales(prices, sales).strip()
    assert result == EXPECTED[tc_name]
