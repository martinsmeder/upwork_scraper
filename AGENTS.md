# Repository Guidelines

## Project State

This repository is a work-in-progress Upwork scraper. The current target behavior is defined in `SPEC.md`, and execution order is tracked in `IMPLEMENTATION-PLAN.md`. New sessions should read those two files first.

Current code status:

- `main.py` is only a minimal Camoufox smoke test that opens Upwork search.
- The real implementation is not complete yet.
- `requirements.txt` reflects the current `venv` and includes `camoufox` and `playwright`.

## Project Structure

Keep top-level files small and purposeful:

- `main.py`: current script entrypoint; intended final CLI is `python3 main.py [query] [card count]`.
- `SPEC.md`: scraper requirements, output schema, selectors, and scope.
- `IMPLEMENTATION-PLAN.md`: ordered checklist of implementation steps.
- `research/`: saved DOM fragments and screenshots used to build selectors safely.
- `notes.txt`: local setup notes.
- `requirements.txt`: pinned dependencies from the active virtual environment.

## Research Files

Prefer the focused artifacts over the large fallback dump:

- `research/card.html`: single collapsed job card.
- `research/card-container.html`: multi-card list fragment.
- `research/navigation.html`: pagination controls.
- `research/full-body.txt`: full page body; use only when broader context is needed.
- `research/upwork-search-full-page.png`: visual reference.

## Development Workflow

Use the checked-in virtual environment unless the user explicitly changes that setup.

Key commands:

- `source venv/bin/activate`
- `python3 main.py "mcp" 10`
- `python -m camoufox fetch`
- `pip freeze > requirements.txt`

## Implementation Notes

Scrape collapsed cards only. Do not open job detail pages in the first version. Page-level collection is preferred over card-by-card interaction: load the list, extract all visible cards in order, click next, repeat.

Store absent fields as `null`. Save outputs as `jobsN.json` without overwriting prior runs.

## Style & Testing

Use Python, 4-space indentation, and PEP 8 names. Keep selector lookup, parsing, pagination, and file output in separate functions. When tests are added, use `pytest` and build parser tests from files in `research/` instead of live network calls.

## Safety

Do not commit secrets, cookies, or private account data. Treat browser state and captured Upwork content as sensitive. Sanitize any saved artifacts before committing them.
