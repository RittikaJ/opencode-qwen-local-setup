# Fix a local log analyzer

This program reads an HTTP access log and reports request count, error count, and the slowest request. It has two bugs. It uses Python's standard library and the bundled sample file; no downloads are needed.

Complete the [main setup](../../README.md), then run each command separately from the repository root in Terminal A. Keep Ollama running in Terminal B.

## Check the starting point

```bash
python3 -m unittest discover -s examples/log-analyzer -v
```

Expected before the fix: **3 failures out of 7 tests**.

## Ask OpenCode to fix it

```bash
.tools/node_modules/.bin/opencode --pure
```

Wait for OpenCode to open, then paste this prompt into it:

```text
Fix examples/log-analyzer/log_analyzer.py using its README. Keep the tests unchanged and don't install anything. Run its tests and explain your fix.
```

The required behavior is:

- Each line has four fields: `METHOD PATH STATUS DURATION_MS`.
- Count valid requests. Count HTTP status codes 400–599 as errors.
- Report the slowest request using its numeric duration in milliseconds. Keep the first on a tie.
- Ignore blank or malformed lines: wrong field count, path without a leading `/`, noninteger status or duration, status outside 100–599, or negative duration.
- Return `{"requests": 0, "errors": 0, "slowest": null}` for no valid requests (`None` in Python).

## Check the result

Exit OpenCode:

```text
/exit
```

Once the terminal prompt returns, run the tests:

```bash
python3 -m unittest discover -s examples/log-analyzer -v
```

Expected after the fix: **7 tests, OK**. Then run the program:

```bash
python3 examples/log-analyzer/log_analyzer.py examples/log-analyzer/sample.log
```

Expected after the fix:

```text
Requests: 6
Errors: 3
Slowest: /export (1200 ms)
```

These are expected results for the exercise, not a record of a completed OpenCode run. For an offline demonstration, perform the OpenCode task with external networking disconnected after completing the tutorial's online setup.
