# Build a CSV sales report

Ask OpenCode to implement a small feature using a local CSV file. Python's standard library is enough; no packages or internet are needed after setup.

`csv_report.py` already opens the file. Its `build_report` function is deliberately unfinished. It should:

- Combine rows for the same product, adding units and revenue (`quantity × unit_price`).
- Use `Decimal` for money and print two decimal places.
- Sort product rows alphabetically and finish with a `TOTAL` row.
- Return a zero total for a file containing only the header.

Inputs have the columns `product,quantity,unit_price`, non-negative integer quantities, and non-negative prices. A product with zero units still gets a row. Return a string without a trailing newline.

## Try it

Use Terminal A in the repository root. Keep Ollama running in Terminal B. Complete the [main setup](../../README.md) before disconnecting.

First, run this example's tests:

```bash
python3 -m unittest discover -s examples/csv-report -v
```

They should fail because `build_report` is unfinished.

Start OpenCode directly:

```bash
.tools/node_modules/.bin/opencode --pure
```

Paste this into OpenCode:

```text
Complete examples/csv-report/csv_report.py using its README. Keep the tests unchanged and don't install anything. Run this example's tests and explain what you changed.
```

When it finishes, enter this inside OpenCode:

```text
/exit
```

Run the tests again in Terminal A:

```bash
python3 -m unittest discover -s examples/csv-report -v
```

Expected after a successful implementation: all seven tests pass.

Then run the report:

```bash
python3 examples/csv-report/csv_report.py
```

Expected output:

```text
Product | Units | Revenue
Mug | 1 | 8.25
Notebook | 3 | 14.00
Pen | 5 | 0.70
TOTAL | 9 | 22.95
```

These are expected results, not a completed OpenCode run.
