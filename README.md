# Stock Report Agent

This repository contains a Stock Report Agent that generates professional, broker-style equity research HTML reports using Yahoo Finance data (via yfinance).

This branch includes robustness fixes (SMA/EMA key bug fix, safe MFI calculation, yfinance attribute fallbacks, peer-info caching, and logging).

Quick start

1. Install dependencies

```bash
pip install -r requirements.txt
# or
pip install yfinance pandas numpy matplotlib pytest
```

2. Generate a single ticker report

```bash
python stock_report_agent.py --ticker AAPL --output reports
```

3. Run tests

```bash
pytest -q
```

Notes

- The script currently embeds charts as base64 PNG images in the generated HTML. For large portfolios this can produce large HTML files. Consider using the `--output` directory to store images separately and referencing them.
- The beta calculation uses a configurable benchmark symbol (default: `^NSEI`). Provide `--benchmark` to override.

Changes in this branch

- Fixed SMA/EMA bullish-count bug (integer vs string keys).
- Made MFI calculation robust to division-by-zero.
- Added yfinance attribute fallbacks (`financials`, `quarterly_financials`, `balance_sheet`).
- Replaced bare except: blocks with `except Exception as e` and lightweight logging.
- Cached peer ticker info in memory to reduce repeated network calls.
- Added plot labels so legends render correctly.

Next steps (suggested)

- Add a CLI flag to write images to files instead of embedding base64.
- Add CI workflow to run tests on push / PR.
- Add more unit tests for financial row detection and HTML rendering.
