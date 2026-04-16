# Repository Guidelines

## Project Structure & Module Organization
This repository is currently a small research-oriented Python workspace. Keep top-level files minimal:

- `README.md`: short project summary.
- `notes.txt`: local workflow notes such as environment setup.
- `research/`: saved HTML snapshots and text extracts used to inspect Upwork page structure.
- `venv/`: local virtual environment for development; treat it as machine-specific and avoid editing installed packages directly.

If scraper code is added, place runtime modules in a dedicated package such as `src/upwork_scraper/` and keep tests under `tests/`.

## Build, Test, and Development Commands
Use the existing virtual environment workflow noted in the repo:

- `source venv/bin/activate`: activate the local Python environment.
- `pip freeze > requirements.txt`: capture dependency versions after adding or upgrading packages.
- `python -m pytest`: run the test suite once `tests/` exists.
- `python -m playwright install`: install browser binaries if Playwright-based scraping is introduced.

Prefer documenting any new repeatable workflow in `README.md` when adding commands.

## Coding Style & Naming Conventions
Use Python with 4-space indentation and PEP 8 naming:

- `snake_case` for modules, functions, and variables.
- `PascalCase` for classes.
- `UPPER_CASE` for constants and environment variable names.

Keep scraping selectors and parsing logic separated so HTML changes are easier to isolate. Favor small functions over large scripts. If you add formatting or linting tools, standardize on one command path such as `ruff check .` and `ruff format .`.

## Testing Guidelines
Use `pytest` for new tests. Name files `test_<feature>.py` and keep fixtures close to the behavior they support. For scraper logic, add regression tests around HTML parsing using saved samples from `research/` instead of live network calls. Run tests locally before opening a PR.

## Commit & Pull Request Guidelines
The current history starts with `Initial commit`, so adopt short, imperative commit messages such as `Add parser for job card HTML`. Keep each commit focused on one change. PRs should include:

- a concise description of the change,
- any setup or dependency updates,
- linked issue or task context when available,
- sample output or screenshots when UI or HTML fixtures change.

## Security & Configuration Tips
Do not commit secrets, session cookies, or captured account data. Store credentials in environment variables, and sanitize research artifacts before committing them.
