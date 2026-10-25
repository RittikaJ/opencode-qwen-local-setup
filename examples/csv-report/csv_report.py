"""Turn a local sales CSV into a small text report.

Complete build_report; the command-line entry point is already provided.
See README.md for the output format and examples.
"""

import argparse
from pathlib import Path


def build_report(csv_text: str) -> str:
    """Group product,quantity,unit_price rows into a sorted sales report.

    Return the header, one row per product, and a TOTAL row. Sum units and
    quantity * unit_price for each product. Use Decimal for money and show
    two decimal places. Sort products alphabetically. Header-only input
    should produce a zero TOTAL. Inputs have valid headers, non-negative
    integer quantities and non-negative decimal prices.
    """
    raise NotImplementedError("Complete build_report using the README and tests.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path", nargs="?", type=Path,
        default=Path(__file__).with_name("sample.csv"),
    )
    args = parser.parse_args()
    print(build_report(args.csv_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
