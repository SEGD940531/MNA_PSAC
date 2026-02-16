# main.py

import json
import sys


def compute_sales(prices, sales):
    """
    Temporary implementation.
    Returns a fixed value until real calculation logic is implemented.
    """
    return "0.00"


def main():
    if len(sys.argv) < 3:
        print("Usage: computeSales <price_file> <sales_file>")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    with open(price_file) as f:
        prices = json.load(f)

    with open(sales_file) as f:
        sales = json.load(f)

    result = compute_sales(prices, sales)
    print(result)


if __name__ == "__main__":
    main()