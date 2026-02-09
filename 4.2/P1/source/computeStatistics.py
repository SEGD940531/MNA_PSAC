import sys
import time
import logging
from pathlib import Path

from statistics_core import mean, median, mode, variance_population, std_population
from file_utils import read_numbers

logging.basicConfig(level=logging.INFO)


def _extract_case_name(input_path: str) -> str:
    """Extract a friendly case name from the input path (e.g., TC1.txt -> TC1)."""
    name = Path(input_path).name
    return name.replace(".txt", "")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]
    case_name = _extract_case_name(file_path)

    start_time = time.time()
    numbers = read_numbers(file_path)

    if not numbers:
        print("No valid numbers found.")
        return

    results = {
        "Mean": mean(numbers),
        "Median": median(numbers),
        "Mode": mode(numbers),
        "VariancePopulation": variance_population(numbers),
        "StdPopulation": std_population(numbers),
    }

    elapsed = time.time() - start_time

    output_lines: list[str] = []
    output_lines.append(f"TestCase: {case_name}")
    for key, value in results.items():
        output_lines.append(f"{key}: {value}")
    output_lines.append(f"ExecutionTimeSeconds: {elapsed}")
    output_lines.append("-" * 60)

    output_text = "\n".join(output_lines)

    print(output_text)

    results_dir = Path("../results")
    results_dir.mkdir(exist_ok=True)

    # Append so all test cases are kept in the same file
    with open(results_dir / "StatisticsResults.txt", "a", encoding="utf-8") as file:
        file.write(output_text + "\n")


if __name__ == "__main__":
    main()