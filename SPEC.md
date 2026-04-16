# Upwork Scraper Specification

## Goal

Build a basic Upwork job search scraper runnable as:

```bash
python3 main.py [query] [card count]
```

The scraper opens a real browser, allows manual completion of any immediate Cloudflare Turnstile challenge, then scrapes data from collapsed search-result cards only and writes the results to a per-run JSON file.

## Inputs

- `query`: free-text search string used on Upwork job search.
- `card count`: total number of job cards to collect across pages.

## Output

- Save results to `jobsN.json`, where `N` is the next available integer for the current directory.
- Do not overwrite previous runs.
- Store a flat JSON array of job objects.

## Required Browser Flow

1. Launch a visible browser session with basic human-like behavior.
2. Open the Upwork search results page for the provided query.
3. Pause if Cloudflare or similar verification blocks access.
4. Resume automatically once the jobs list is visible.
5. Scrape the current page from the collapsed cards only.
6. Move to the next results page and repeat until the requested card count is reached or pagination ends.

## Human-Like Interaction Scope

The automation should mimic a simple human workflow for each results page:

- open the page,
- allow manual verification,
- move the mouse naturally,
- bring focus to the visible results list,
- copy the page worth of visible cards in one pass,
- click the next page control,
- repeat.

No per-card clicking or per-card delay is required. Human-like behavior should be added around page setup, list interaction, and pagination only.

The browser session should remain:

- visible,
- foregrounded,
- single-tab,
- free of background polling,
- free of auto-refresh,
- free of hidden retries.

## Human Interaction Timing

Use page-level delays only, with slight randomized jitter inside each range:

- after initial page load, before first meaningful interaction: roughly 2-5 seconds
- after `JobsList` becomes visible and before extraction starts: roughly 1-3 seconds
- before clicking the next page control: roughly 2-5 seconds
- after next-page navigation and before extraction resumes: roughly 1-3 seconds

Small cursor movement, hover, and list-focusing behavior should be used to make page interaction look like a human preparing to copy the visible results. The implementation should avoid large fixed sleeps and should prefer bounded random delays plus Playwright locator waiting.

## List Stability Requirement

Extraction must begin only after `JobsList` is both visible and stable. Stability means the results container is present, the visible cards have rendered, and pagination-triggered updates have settled before scraping starts.

## Extraction Scope

Only collect data present in collapsed search cards. Do not open job details pages.

Each job object should include all available collapsed-card fields, with these minimum keys:

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

If a field is absent for a given card, store `null`.

## DOM Assumptions From Research

Initial selectors can be based on the saved research artifacts:

- jobs list container: `section[data-test="JobsList"]`
- job card: `article[data-test="JobTile"]`
- title link: `a[data-test="job-tile-title-link UpLink"]`
- job info list: `[data-test="JobInfo"]`
- next page control: `[data-test="next-page"]`

The implementation should tolerate minor markup variation where practical.

## Research References

The `research/` directory contains the saved artifacts that define the first implementation:

- `research/card.html`: one collapsed job card, useful for field-level extraction rules.
- `research/card-container.html`: a multi-card list fragment, useful for list traversal and per-card ordering.
- `research/navigation.html`: pagination markup, including controls such as `prev-page`, `pagination-item`, and `next-page`.
- `research/full-body.txt`: full saved page body for fallback inspection when container-level context is needed.
- `research/upwork-search-full-page.png`: screenshot of the search results page for visual debugging.

Prefer `card.html`, `card-container.html`, and `navigation.html` for day-to-day development. Use `full-body.txt` only when broader page context is required.

## Pagination Rules

- Scrape cards in on-page order.
- Stop exactly at the requested `card count`.
- If fewer cards exist than requested, return all collected cards and exit cleanly.
- Track page number and within-page position for debugging.

## Non-Goals For First Version

- Logging in.
- Opening individual job pages.
- Deduplication across separate runs.
- Database storage.
- Advanced retry orchestration.

## Success Criteria

A run is successful when:

- the browser opens visibly,
- the script waits through manual verification if needed,
- the requested number of collapsed cards is collected when available,
- and a new `jobsN.json` file is written with structured job data.
