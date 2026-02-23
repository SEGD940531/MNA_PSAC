import os
import sys

from .app import run_tui


def main() -> None:
    base_dir = os.getenv("STORAGE_DIR", "store")
    sys.exit(run_tui(base_dir))


if __name__ == "__main__":
    main()