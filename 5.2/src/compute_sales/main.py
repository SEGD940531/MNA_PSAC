# compute_sales/main.py

from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, Iterable, List


def _as_decimal(value: Any) -> Decimal:
    """
    Convert common numeric types to Decimal safely.
    Using str(value) avoids binary float rounding artifacts.
    """
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def _build_price_map(prices: Any) -> Dict[str, Decimal]:
    """
    Builds a map: product_title -> price (Decimal)

    Expected input:
      prices = [ { "title": "...", "price": 28.1, ... }, ... ]

    Defensive: supports common wrapper keys if `prices` is a dict.
    """
    items: Iterable[dict]

    if isinstance(prices, list):
        items = prices
    elif isinstance(prices, dict):
        for key in ("products", "ProductList", "items", "data"):
            if isinstance(prices.get(key), list):
                items = prices[key]
                break
        else:
            items = []
    else:
        items = []

    price_map: Dict[str, Decimal] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        title = item.get("title")
        if not isinstance(title, str) or not title.strip():
            continue

        price = _as_decimal(item.get("price"))
        price_map[title] = price

    return price_map


def compute_sales(prices: Any, sales: Any) -> str:
    """
    Compute the total sales amount as a string with 2 decimals.

    Rules:
    - Only count rows where Product exists in the catalogue
    - Quantity must be numeric; positive adds, negative subtracts (returns)
    - Quantity == 0 is ignored
    - Unknown products or invalid rows are ignored
    """
    price_map = _build_price_map(prices)

    if isinstance(sales, list):
        sales_items: List[dict] = sales
    elif isinstance(sales, dict):
        for key in ("sales", "Sales", "records", "data", "items"):
            if isinstance(sales.get(key), list):
                sales_items = sales[key]
                break
        else:
            sales_items = []
    else:
        sales_items = []

    total = Decimal("0")

    for row in sales_items:
        if not isinstance(row, dict):
            continue

        product = row.get("Product")
        if not isinstance(product, str) or product not in price_map:
            continue

        qty = _as_decimal(row.get("Quantity"))
        if qty == 0:
            continue

        total += price_map[product] * qty

    total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{total:.2f}"
