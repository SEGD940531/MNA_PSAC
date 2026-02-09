import sys
import time
import logging
from pathlib import Path

from wordcount_core import tokenize, count_words, sort_counts

logging.basicConfig(level=logging.INFO)


def _read_text(file_path: str) -> str:
    """Read all text content from a file."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    return path.read_text(encoding="utf-8", errors="replace")


def _extract_case_name(input_path: str) -> str:
    """Extract a friendly case name from the input path (e.g., TC1.txt -> TC1)."""
    name = Path(input_path).name
    if name.lower().endswith(".txt"):
        return name[:-4]
    return name


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    case_name = _extract_case_name(input_file)

    start_time = time.time()

    try:
        content = _read_text(input_file)
    except (OSError, FileNotFoundError) as exc:
        logging.error("Failed to read input file: %s", exc)
        sys.exit(1)

    tokens = tokenize(content)

    if not tokens:
        # Req 3: show error but continue execution
        print("ERROR: No valid words found in input.", file=sys.stderr)

    counts = count_words(tokens)
    sorted_results = sort_counts(counts)

    elapsed = time.time() - start_time

    # Output (tab-separated)
    output_lines: list[str] = []
    output_lines.append(f"===== TEST CASE: {case_name} =====")
    output_lines.append("WORD\tFREQUENCY")
    for item in sorted_results:
        output_lines.append(f"{item.word}\t{item.count}")

    output_lines.append("")
    output_lines.append(f"DistinctWords:\t{len(sorted_results)}")
    output_lines.append(f"TotalWords:\t{len(tokens)}")
    output_lines.append(f"ExecutionTimeSeconds:\t{elapsed}")

    output_text = "\n".join(output_lines)

    # Req 2: print on screen
    print(output_text)

    # Write evidence file in required location
    results_dir = Path("../results")
    results_dir.mkdir(exist_ok=True)
    output_path = results_dir / "WordCountResults.txt"

    # Append so multiple TCs do not overwrite evidence
    with open(output_path, "a", encoding="utf-8") as file:
        if output_path.exists() and output_path.stat().st_size > 0:
            file.write("\n\n")
        file.write(output_text)
        file.write("\n")


if __name__ == "__main__":
    main()