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

## Tooling Note

`apply_patch` may fail in this repo with a sandbox mismatch error from the helper, even for simple file creates or updates. When that happens:

- do not keep retrying `apply_patch`
- use direct shell-based file edits instead, for example `python3 - <<'PY'` with `Path(...).write_text(...)` or a targeted heredoc rewrite
- if a new file is needed, create it with shell tooling first
- verify the final file contents after writing

Future sessions should treat this as an environment/tooling issue, not a patch-formatting issue.

## Safety

Do not commit secrets, cookies, or private account data. Treat browser state and captured Upwork content as sensitive. Sanitize any saved artifacts before committing them.
