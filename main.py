import json
import random
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.parse import urljoin

from camoufox.sync_api import Camoufox
from playwright.sync_api import Locator
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

UPWORK_BASE_URL = "https://www.upwork.com"
JOB_CARD_SELECTOR = 'article[data-test="JobTile"]'
NEXT_PAGE_SELECTOR = '[data-test="next-page"]'
TITLE_LINK_SELECTOR = 'a[data-test="job-tile-title-link UpLink"]'
POSTED_SELECTOR = 'small[data-test="job-pubilshed-date"]'
DESCRIPTION_SELECTOR = '[data-test="UpCLineClamp JobDescription"] p'
DEFAULT_QUERY = "mcp"
DEFAULT_CARD_COUNT = 10
INITIAL_PAGE_DELAY_RANGE = (1.5, 3.0)
CARD_SCAN_DELAY_RANGE = (0.15, 0.35)
PRE_NEXT_PAGE_DELAY_RANGE = (1.5, 3.0)
POST_PAGE_CHANGE_DELAY_RANGE = (1.0, 2.0)
WAIT_TIMEOUT_MS = 5 * 60 * 1000
OUTPUT_DIRECTORY_NAME = "output"
OUTPUT_FILE_PREFIX = "jobs"
OUTPUT_FILE_SUFFIX = ".json"
RESULTS_PER_PAGE = 50
SEARCH_FILTERS = {
    "amount": "500-",
    "client_hires": "10-",
    "hourly_rate": "30-",
    "sort": "recency",
    "t": "0,1",
}
QUERY_PREFIX = "title:("
QUERY_SUFFIX = ")"
SEARCH_PATH = "/nx/search/jobs"


def parse_args() -> tuple[str, int]:
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY

    if len(sys.argv) > 2:
        try:
            card_count = int(sys.argv[2])
        except ValueError as exc:
            raise SystemExit("card count must be an integer") from exc

        if card_count <= 0:
            raise SystemExit("card count must be greater than zero")
    else:
        card_count = DEFAULT_CARD_COUNT

    return query, card_count


def build_search_url(query: str, page_number: int = 1) -> str:
    formatted_query = f"{QUERY_PREFIX}{query}{QUERY_SUFFIX}"
    params = {
        **SEARCH_FILTERS,
        "page": page_number,
        "per_page": RESULTS_PER_PAGE,
        "q": formatted_query,
    }
    return f"{UPWORK_BASE_URL}{SEARCH_PATH}?{urlencode(params)}"


def random_delay(range_seconds: tuple[float, float]) -> int:
    minimum, maximum = range_seconds
    return int(random.uniform(minimum, maximum) * 1000)


def human_pause(page: Page, range_seconds: tuple[float, float]) -> None:
    page.wait_for_timeout(random_delay(range_seconds))


def wait_for_job_cards(page: Page) -> None:
    try:
        page.locator(JOB_CARD_SELECTOR).first.wait_for(state="visible", timeout=WAIT_TIMEOUT_MS)
    except PlaywrightTimeoutError as exc:
        raise SystemExit(
            "Timed out waiting for visible Upwork job cards. "
            "Complete any manual verification and try again."
        ) from exc


def move_mouse_to_locator(page: Page, locator: Locator) -> None:
    box = locator.bounding_box()
    if box is None:
        return

    target_x = box["x"] + random.uniform(box["width"] * 0.2, box["width"] * 0.8)
    target_y = box["y"] + random.uniform(box["height"] * 0.2, box["height"] * 0.8)
    page.mouse.move(target_x, target_y, steps=random.randint(12, 24))


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = " ".join(value.split())
    return cleaned or None


def get_optional_text(locator: Locator) -> str | None:
    if locator.count() == 0 or not locator.first.is_visible():
        return None

    return clean_text(locator.first.inner_text())


def strip_prefix(value: str | None, prefix: str) -> str | None:
    if value is None:
        return None

    if value.startswith(prefix):
        return clean_text(value.removeprefix(prefix))

    return value


def extract_job_type_and_budget(card: Locator) -> tuple[str | None, str | None]:
    job_type_text = get_optional_text(card.locator('[data-test="job-type-label"]'))
    fixed_budget_text = strip_prefix(
        get_optional_text(card.locator('[data-test="is-fixed-price"]')),
        "Est. budget:",
    )

    if job_type_text is None:
        return None, fixed_budget_text

    if job_type_text.startswith("Hourly:"):
        return "Hourly", clean_text(job_type_text.removeprefix("Hourly:"))

    if job_type_text == "Fixed price":
        return job_type_text, fixed_budget_text

    return job_type_text, fixed_budget_text


def extract_posted(card: Locator) -> str | None:
    posted_text = get_optional_text(card.locator(POSTED_SELECTOR))

    if posted_text is None:
        return None

    if posted_text.startswith("Posted "):
        return clean_text(posted_text.removeprefix("Posted "))

    return posted_text


def extract_duration(card: Locator) -> str | None:
    return strip_prefix(
        get_optional_text(card.locator('[data-test="duration-label"]')),
        "Est. time:",
    )


def extract_job(card: Locator, query: str, page_number: int, position: int) -> dict:
    title_link = card.locator(TITLE_LINK_SELECTOR)
    title = get_optional_text(title_link)
    relative_job_url = title_link.first.get_attribute("href") if title_link.count() else None
    job_type, budget_or_rate = extract_job_type_and_budget(card)
    raw_page_number = card.get_attribute("data-ev-page_number")
    raw_position = card.get_attribute("data-ev-position")

    return {
        "nr": None,
        "query": query,
        "page": int(raw_page_number) if raw_page_number and raw_page_number.isdigit() else page_number,
        "position": int(raw_position) if raw_position and raw_position.isdigit() else position,
        "job_id": card.get_attribute("data-test-key") or card.get_attribute("data-ev-job-uid"),
        "title": title,
        "job_url": urljoin(UPWORK_BASE_URL, relative_job_url) if relative_job_url else None,
        "posted": extract_posted(card),
        "job_type": job_type,
        "experience_level": get_optional_text(card.locator('[data-test="experience-level"]')),
        "budget_or_rate": budget_or_rate,
        "duration": extract_duration(card),
        "description": get_optional_text(card.locator(DESCRIPTION_SELECTOR)),
    }


def extract_jobs(page: Page, query: str, page_number: int, limit: int) -> list[dict]:
    jobs: list[dict] = []
    cards = page.locator(JOB_CARD_SELECTOR)

    for index in range(cards.count()):
        if len(jobs) >= limit:
            break

        card = cards.nth(index)
        if not card.is_visible():
            continue

        card.scroll_into_view_if_needed()
        human_pause(page, CARD_SCAN_DELAY_RANGE)
        jobs.append(extract_job(card, query, page_number, len(jobs) + 1))

    return jobs


def go_to_next_page(page: Page) -> bool:
    next_page = page.locator(NEXT_PAGE_SELECTOR)
    if next_page.count() == 0:
        return False

    next_button = next_page.first
    if next_button.get_attribute("aria-disabled") == "true":
        return False

    next_href = next_button.get_attribute("href")
    if not next_href:
        return False

    expected_url = urljoin(UPWORK_BASE_URL, next_href)

    next_button.scroll_into_view_if_needed()
    human_pause(page, PRE_NEXT_PAGE_DELAY_RANGE)
    move_mouse_to_locator(page, next_button)
    next_button.hover()
    next_button.click(delay=random.randint(60, 160))
    page.wait_for_url(expected_url, wait_until="domcontentloaded", timeout=WAIT_TIMEOUT_MS)
    wait_for_job_cards(page)
    human_pause(page, POST_PAGE_CHANGE_DELAY_RANGE)
    return True


def next_output_path(directory: Path) -> Path:
    next_index = 1

    while True:
        candidate = directory / f"{OUTPUT_FILE_PREFIX}{next_index}{OUTPUT_FILE_SUFFIX}"
        if not candidate.exists():
            return candidate
        next_index += 1


def save_jobs(jobs: list[dict], directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    output_path = next_output_path(directory)
    output_path.write_text(json.dumps(jobs, indent=2) + "\n", encoding="utf-8")
    return output_path


def assign_job_numbers(jobs: list[dict]) -> list[dict]:
    for index, job in enumerate(jobs, start=1):
        job["nr"] = index

    return jobs


def run(query: str, card_count: int) -> tuple[Path, int]:
    jobs: list[dict] = []
    current_page = 1

    with Camoufox(headless=False) as browser:
        page = browser.new_page()
        page.goto(build_search_url(query, current_page), wait_until="domcontentloaded")
        wait_for_job_cards(page)
        human_pause(page, INITIAL_PAGE_DELAY_RANGE)

        while len(jobs) < card_count:
            remaining_slots = card_count - len(jobs)
            page_jobs = extract_jobs(page, query, current_page, remaining_slots)
            if not page_jobs:
                break

            jobs.extend(page_jobs)
            if len(jobs) >= card_count:
                break

            if not go_to_next_page(page):
                break

            current_page += 1

    numbered_jobs = assign_job_numbers(jobs)
    output_path = save_jobs(numbered_jobs, Path.cwd() / OUTPUT_DIRECTORY_NAME)
    return output_path, len(jobs)


def main() -> None:
    query, card_count = parse_args()

    try:
        output_path, job_count = run(query, card_count)
    except OSError as exc:
        print(f"Failed to save results: {exc}")
        raise SystemExit(1) from exc

    print(f"Saved {job_count} jobs to {output_path}")


if __name__ == "__main__":
    main()
