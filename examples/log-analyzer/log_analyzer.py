"""Summarize local HTTP request logs. This starter contains intentional bugs."""

import argparse
from pathlib import Path


def analyze_logs(lines):
    """Return requests, errors (status >= 400), and the slowest request.

    Each valid line is METHOD PATH STATUS DURATION_MS. PATH starts with /,
    STATUS is an integer from 100 to 599, and DURATION_MS is a nonnegative
    integer. Ignore blank or malformed lines. Keep the first request when
    durations tie. With no valid requests, slowest is None.
    """
    report = {"requests": 0, "errors": 0, "slowest": None}
    for line in lines:
        fields = line.split()
        if len(fields) != 4:
            continue
        method, path, status_text, duration_text = fields
        try:
            status = int(status_text)
            duration = int(duration_text)
        except ValueError:
            continue
        if not path.startswith("/") or not 100 <= status <= 599 or duration < 0:
            continue

        report["requests"] += 1
        if status > 400:
            report["errors"] += 1
        if report["slowest"] is None or duration_text > str(report["slowest"]["duration_ms"]):
            report["slowest"] = {"path": path, "duration_ms": duration}
    return report


def main():
    parser = argparse.ArgumentParser(description="Summarize an HTTP access log.")
    parser.add_argument("log_file", type=Path)
    args = parser.parse_args()
    with args.log_file.open(encoding="utf-8") as stream:
        report = analyze_logs(stream)
    print(f"Requests: {report['requests']}")
    print(f"Errors: {report['errors']}")
    slowest = report["slowest"]
    if slowest is None:
        print("Slowest: none")
    else:
        print(f"Slowest: {slowest['path']} ({slowest['duration_ms']} ms)")


if __name__ == "__main__":
    main()
