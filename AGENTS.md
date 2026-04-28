# Repository Guidelines

## Project Structure & Module Organization

This repository is centered on [`main.py`](/home/martin/repos/upwork_scraper/main.py), a Python Upwork scraper that collects collapsed job cards and saves them to `output/jobsN.json`. [`README.md`](/home/martin/repos/upwork_scraper/README.md) documents setup and usage. [`data-processing.md`](/home/martin/repos/upwork_scraper/data-processing.md) defines the workflow for classifying scraped JSON files and producing summary files. Treat `output/` as generated local data.

## Build, Test, and Development Commands

Use the checked-in `venv`:

```bash
source venv/bin/activate
pip install -r requirements.txt
python3 main.py "mcp" 10
python -m camoufox fetch
```

- `pip install -r requirements.txt`: install Python dependencies.
- `python -m camoufox fetch`: fetch Camoufox browser assets.
- `python3 main.py "full stack" 75`: run the scraper from the repo root.

## Coding Style & Naming Conventions

Use Python with 4-space indentation and PEP 8 names. Prefer small functions for parsing, pagination, and output. Use `snake_case` for functions and variables, `UPPER_SNAKE_CASE` for constants, and keep selector logic readable and local to the scraper flow.

## Testing Guidelines

There is no formal test suite yet. Validate scraper changes by running `main.py` locally and checking the generated JSON. If tests are added later, prefer `pytest` and fixture-based parsing tests over live network calls.

## Commit & Pull Request Guidelines

Keep commits short and direct, matching existing history such as `Updated gitignore` or `Added demand summary`. Keep each commit scoped to one logical change. PRs should state what changed, how it was verified, and whether output or classification files were regenerated.

## Data Processing Notes

For dataset work, classify jobs using the combined `title` and `description`, assign exactly one `delivery_type` and one `solution_category`, then save `*-classified.json` and `*-summary.json` in `output/`. Keep labels consistent within a file.
