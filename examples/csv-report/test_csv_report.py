import subprocess
import sys
import unittest
from pathlib import Path

from csv_report import build_report


HERE = Path(__file__).resolve().parent
SAMPLE_REPORT = (
    "Product | Units | Revenue\n"
    "Mug | 1 | 8.25\n"
    "Notebook | 3 | 14.00\n"
    "Pen | 5 | 0.70\n"
    "TOTAL | 9 | 22.95"
)


class CsvReportTests(unittest.TestCase):
    def test_sample_report(self):
        self.assertEqual(
            build_report((HERE / "sample.csv").read_text(encoding="utf-8")),
            SAMPLE_REPORT,
        )

    def test_groups_product_rows_with_different_prices(self):
        data = "product,quantity,unit_price\nTea,2,3.50\nTea,1,4.00\n"
        self.assertEqual(
            build_report(data),
            "Product | Units | Revenue\nTea | 3 | 11.00\nTOTAL | 3 | 11.00",
        )

    def test_decimal_prices(self):
        data = "product,quantity,unit_price\nToken,3,0.10\nToken,1,0.20\n"
        self.assertEqual(
            build_report(data),
            "Product | Units | Revenue\nToken | 4 | 0.50\nTOTAL | 4 | 0.50",
        )
        self.assertEqual(
            build_report("product,quantity,unit_price\nToken,1,2.675\n"),
            "Product | Units | Revenue\nToken | 1 | 2.68\nTOTAL | 1 | 2.68",
        )

    def test_header_only(self):
        self.assertEqual(
            build_report("product,quantity,unit_price\n"),
            "Product | Units | Revenue\nTOTAL | 0 | 0.00",
        )

    def test_alphabetical_order(self):
        data = "product,quantity,unit_price\nZebra,1,2.00\nApple,2,1.00\n"
        self.assertEqual(
            build_report(data),
            "Product | Units | Revenue\nApple | 2 | 2.00\nZebra | 1 | 2.00\nTOTAL | 3 | 4.00",
        )

    def test_zero_quantity(self):
        data = "product,quantity,unit_price\nMug,0,8.25\n"
        self.assertEqual(
            build_report(data),
            "Product | Units | Revenue\nMug | 0 | 0.00\nTOTAL | 0 | 0.00",
        )

    def test_cli_prints_sample_report(self):
        result = subprocess.run(
            [sys.executable, str(HERE / "csv_report.py")],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, SAMPLE_REPORT + "\n")


if __name__ == "__main__":
    unittest.main()
