import sys
import time
import logging
from pathlib import Path

from converter_core import parse_int_strict, convert_number

logging.basicConfig(level=logging.INFO)


def _read_lines(file_path: str) -> list[str]:
    """Read all lines from a text file."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    return path.read_text(encoding="utf-8").splitlines()


def _extract_case_name(input_path: str) -> str:
    """Extract a friendly case name from the input path (e.g., TC1.txt -> TC1)."""
    name = Path(input_path).name
    return name.replace(".txt", "")


def _needs_separator(output_path: Path) -> bool:
    """
    Decide if we should add a blank line separator before appending.
    If the file exists and has content, add a separator.
    """
    if not output_path.exists():
        return False
    return output_path.stat().st_size > 0


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    case_name = _extract_case_name(input_file)

    start_time = time.time()

    try:
        lines = _read_lines(input_file)
    except (OSError, FileNotFoundError) as exc:
        logging.error("Failed to read input file: %s", exc)
        sys.exit(1)

    results_dir = Path("../results")
    results_dir.mkdir(exist_ok=True)
    output_path = results_dir / "ConvertionResults.txt"

    # Format similar to the reference: ITEM <TC> BIN HEX
    # Output is tab-separated for easy paste into Excel.
    output_lines: list[str] = [f"ITEM\t{case_name}\tBIN\tHEX"]

    valid_count = 0
    error_count = 0

    item_index = 0
    for idx, line in enumerate(lines, start=1):
        number = parse_int_strict(line)
        if number is None:
            error_count += 1
            # Req 3: show errors but continue
            print(f"ERROR line {idx}: invalid data -> {line!r}", file=sys.stderr)
            continue

        item_index += 1
        conv = convert_number(number)

        # Row format:
        # ITEM  <original decimal>  <binary>  <hex>
        output_lines.append(
            f"{item_index}\t{conv.decimal}\t{conv.binary}\t{conv.hexadecimal}"
        )
        valid_count += 1

    elapsed = time.time() - start_time

    output_lines.append("")
    output_lines.append(f"ValidItems:\t{valid_count}")
    output_lines.append(f"InvalidItems:\t{error_count}")
    output_lines.append(f"ExecutionTimeSeconds:\t{elapsed}")

    output_text = "\n".join(output_lines)

    # Req 2: print on screen
    print(output_text)

    # Append to a single ConvertionResults.txt (do not overwrite)
    with open(output_path, "a", encoding="utf-8") as file:
        if _needs_separator(output_path):
            file.write("\n")

        file.write(f"===== TEST CASE: {case_name} =====\n")
        file.write(output_text)
        file.write("\n")


if __name__ == "__main__":
    main()