# computeSales.py
#
# CLI entrypoint required by assignment.
# Usage:
#   python computeSales.py priceCatalogue.json salesRecord.json

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any,  List, Tuple

from compute_sales import compute_sales


def _print_err(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)


def _print_warn(msg: str) -> None:
    print(f"[WARN] {msg}", file=sys.stderr)


def _load_json_file(path: str) -> Any:
    """
    Load JSON defensively.
    If the file is unreadable or invalid JSON, return [] and print error.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        _print_err(f"File not found: {path}")
    except json.JSONDecodeError as e:
        _print_err(f"Invalid JSON in {path}: {e}")
    except OSError as e:
        _print_err(f"Could not read {path}: {e}")
    return []


def _validate_prices(prices: Any) -> Tuple[Any, List[str]]:
    """
    Best-effort validation for price catalogue.
    We do not stop execution; we collect warnings and continue.
    """
    warnings: List[str] = []

    if isinstance(prices, list):
        for i, item in enumerate(prices):
            if not isinstance(item, dict):
                warnings.append(f"prices[{i}] is not an object; it will be ignored")
                continue
            title = item.get("title")
            price = item.get("price")
            if not isinstance(title, str) or not title.strip():
                warnings.append(f"prices[{i}].title is missing/invalid; item may be ignored")
            if not isinstance(price, (int, float, str)):
                warnings.append(f"prices[{i}].price is missing/invalid; item may be ignored")
        return prices, warnings

    if isinstance(prices, dict):
        # Some formats wrap the list
        for key in ("products", "ProductList", "items", "data"):
            if isinstance(prices.get(key), list):
                return _validate_prices(prices[key])

    warnings.append("price catalogue is not a list; program will continue with empty catalogue")
    return [], warnings


def _validate_sales(sales: Any) -> Tuple[Any, List[str]]:
    """
    Best-effort validation for sales records.
    We do not stop execution; we collect warnings and continue.
    """
    warnings: List[str] = []

    if isinstance(sales, list):
        for i, row in enumerate(sales):
            if not isinstance(row, dict):
                warnings.append(f"sales[{i}] is not an object; it will be ignored")
                continue
            product = row.get("Product")
            qty = row.get("Quantity")
            if not isinstance(product, str) or not product.strip():
                warnings.append(f"sales[{i}].Product is missing/invalid; row may be ignored")
            # qty can be negative (returns) or positive; we just warn if it's not numeric-ish
            if not isinstance(qty, (int, float, str)):
                warnings.append(f"sales[{i}].Quantity is missing/invalid; row may be ignored")
        return sales, warnings

    if isinstance(sales, dict):
        for key in ("sales", "Sales", "records", "data", "items"):
            if isinstance(sales.get(key), list):
                return _validate_sales(sales[key])

    warnings.append("sales record is not a list; program will continue with empty sales")
    return [], warnings


def _format_human_output(
    price_file: str,
    sales_file: str,
    total: str,
    elapsed_sec: float,
    warnings: List[str],
) -> str:
    lines: List[str] = []
    lines.append("Compute Sales Results")
    lines.append("====================")
    lines.append(f"Price catalogue: {price_file}")
    lines.append(f"Sales record:    {sales_file}")
    lines.append("")
    lines.append(f"TOTAL: {total}")
    lines.append(f"Elapsed time: {elapsed_sec:.6f} seconds")
    lines.append("")

    if warnings:
        lines.append("Warnings")
        lines.append("--------")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def _write_results_file(output_text: str) -> Path:
    """
    Requirement says: write to 'SalesResults.txt'.
    We'll write it to ./output/SalesResults.txt if output/ exists or can be created,
    otherwise fallback to ./SalesResults.txt.
    """
    out_dir = Path("output")
    out_path = out_dir / "SalesResults.txt"

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_text, encoding="utf-8")
        return out_path
    except OSError as e:
        _print_warn(f"Could not write to {out_path}: {e}. Falling back to ./SalesResults.txt")
        fallback = Path("SalesResults.txt")
        fallback.write_text(output_text, encoding="utf-8")
        return fallback


def main() -> int:
    if len(sys.argv) < 3:
        _print_err("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        return 1

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    start = time.perf_counter()

    prices_raw = _load_json_file(price_file)
    sales_raw = _load_json_file(sales_file)

    prices, price_warnings = _validate_prices(prices_raw)
    sales, sales_warnings = _validate_sales(sales_raw)
    warnings = price_warnings + sales_warnings

    # Compute (pure logic lives in package; already tested)
    total = compute_sales(prices, sales)

    elapsed = time.perf_counter() - start

    output_text = _format_human_output(
        price_file=price_file,
        sales_file=sales_file,
        total=total,
        elapsed_sec=elapsed,
        warnings=warnings,
    )

    # Print to screen
    print(output_text)

    # Print to file SalesResults.txt
    out_path = _write_results_file(output_text)
    print(f"Results file: {out_path}")

    # Execution continues even with warnings/errors; only hard CLI usage errors exit non-zero.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
