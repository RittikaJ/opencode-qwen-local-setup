import subprocess
import sys
import unittest
from pathlib import Path

from log_analyzer import analyze_logs

HERE = Path(__file__).resolve().parent


class LogAnalyzerTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(
            analyze_logs([]), {"requests": 0, "errors": 0, "slowest": None}
        )

    def test_counts_every_valid_request(self):
        report = analyze_logs([
            "GET / 200 5", "POST /save 201 7", "GET /old 301 3"
        ])
        self.assertEqual(report["requests"], 3)
        self.assertEqual(report["errors"], 0)

    def test_counts_400_and_later_as_errors(self):
        report = analyze_logs([
            "GET / 200 1", "POST /bad 400 2",
            "GET /missing 404 3", "GET /failed 500 4"
        ])
        self.assertEqual(report["errors"], 3)

    def test_slowest_uses_numeric_duration(self):
        report = analyze_logs([
            "GET /fast 200 9", "GET /medium 200 99", "GET /slow 200 1200"
        ])
        self.assertEqual(report["slowest"], {"path": "/slow", "duration_ms": 1200})

    def test_ignores_blank_and_malformed_lines(self):
        report = analyze_logs([
            "", "   ", "missing fields", "GET / x 10", "GET / 200 slow",
            "GET / 200 -1", "GET / 99 10", "GET / 600 10",
            "GET relative 200 10", "GET / 200 10 extra",
            "GET   /valid   200   15",
        ])
        self.assertEqual(report, {
            "requests": 1, "errors": 0,
            "slowest": {"path": "/valid", "duration_ms": 15},
        })

    def test_first_request_wins_a_duration_tie(self):
        report = analyze_logs(["GET /first 200 20", "GET /second 200 20"])
        self.assertEqual(report["slowest"], {"path": "/first", "duration_ms": 20})

    def test_sample_log_cli(self):
        result = subprocess.run(
            [sys.executable, "-B", str(HERE / "log_analyzer.py"), str(HERE / "sample.log")],
            check=True, capture_output=True, text=True,
        )
        self.assertEqual(result.stdout, "Requests: 6\nErrors: 3\nSlowest: /export (1200 ms)\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
