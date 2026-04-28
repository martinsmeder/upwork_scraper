# Upwork Scraper

Upwork job search scraper for collapsed cards.

The current version:

- opens a real Camoufox browser window
- waits for manual verification if Upwork or Cloudflare blocks the page
- scrapes collapsed job cards only
- requests search pages with `per_page=50`
- paginates by scrolling to the next-page link, moving the mouse to it, clicking it, and waiting for the next page to load
- stops when the requested total number of cards has been collected or pagination ends
- writes results to `output/jobsN.json` without overwriting prior runs

## Requirements

- Python 3
- the checked-in `venv`
- installed dependencies from `requirements.txt`
- Camoufox browser assets fetched locally

## Setup

```bash
source venv/bin/activate
python -m camoufox fetch
```

If dependencies need to be reinstalled:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run from the repository root:

```bash
source venv/bin/activate
python3 main.py "query" count
```

Arguments:

- `query`: free-text title search query; the scraper wraps it as `title:(...)`
- `jobs count`: total number of collapsed job cards to collect across pages

Example:

```bash
python3 main.py "full stack" 150
```

## Output

Results are written to:

```text
output/jobs1.json
output/jobs2.json
output/jobs3.json
...
```

Each run creates the next available file and does not overwrite previous results.

The output is a flat JSON array of job objects with these keys:

- `nr`
- `query`
- `page`
- `position`
- `job_id`
- `title`
- `job_url`
- `posted`
- `job_type`
- `experience_level`
- `budget_or_rate`
- `duration`
- `description`

Missing fields are stored as `null`.

## Notes

- The scraper currently relies on Upwork honoring `per_page=50`. If fewer cards render, it continues with however many are available.
- The search query passed on the command line is wrapped into a title search, for example `"full stack"` becomes `title:(full stack)`.
- Browser interaction is intentionally page-level only to reduce unnecessary actions.
