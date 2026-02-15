import json
from compute_sales.main import compute_sales

def test_small_case():
    with open("tests/fixtures/valid/price_small.json") as f:
        prices = json.load(f)

    with open("tests/fixtures/valid/sales_small.json") as f:
        sales = json.load(f)

    result = compute_sales(prices, sales)

    with open("tests/expected/expected_small.txt") as f:
        expected = f.read()

    assert result.strip() == expected.strip()