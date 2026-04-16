import json
import random
import sys
from pathlib import Path
from urllib.parse import quote_plus
from urllib.parse import urljoin

from camoufox.sync_api import Camoufox
from playwright.sync_api import Locator
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

UPWORK_BASE_URL = "https://www.upwork.com"
JOBS_LIST_SELECTOR = 'section[data-test="JobsList"]'
JOB_CARD_SELECTOR = 'article[data-test="JobTile"]'
NEXT_PAGE_SELECTOR = '[data-test="next-page"]'
TITLE_LINK_SELECTOR = 'a[data-test="job-tile-title-link UpLink"]'
POSTED_SELECTOR = 'small[data-test="job-pubilshed-date"]'
DESCRIPTION_SELECTOR = '[data-test="UpCLineClamp JobDescription"] p'
DEFAULT_QUERY = "mcp"
DEFAULT_CARD_COUNT = 10
INITIAL_INTERACTION_DELAY_RANGE = (2.0, 5.0)
POST_LIST_DELAY_RANGE = (1.0, 3.0)
PRE_NEXT_PAGE_DELAY_RANGE = (2.0, 5.0)
WAIT_TIMEOUT_MS = 5 * 60 * 1000
OUTPUT_DIRECTORY_NAME = "output"
OUTPUT_FILE_PREFIX = "jobs"
OUTPUT_FILE_SUFFIX = ".json"


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


def build_search_url(query: str) -> str:
    encoded_query = quote_plus(query)
    return f"https://www.upwork.com/nx/search/jobs/?q={encoded_query}"


def random_delay(range_seconds: tuple[float, float]) -> float:
    minimum, maximum = range_seconds
    return random.uniform(minimum, maximum)


def wait_for_jobs_list(page) -> None:
    try:
        page.locator(JOBS_LIST_SELECTOR).wait_for(
            state="visible",
            timeout=WAIT_TIMEOUT_MS,
        )
    except PlaywrightTimeoutError as exc:
        raise SystemExit(
            "Timed out waiting for the Upwork jobs list. "
            "Complete any manual verification and try again."
        ) from exc


def wait_for_list_stability(page: Page) -> None:
    jobs_list = page.locator(JOBS_LIST_SELECTOR)
    jobs_list.wait_for(state="visible", timeout=WAIT_TIMEOUT_MS)
    page.wait_for_function(
        """
        (selector) => {
            const list = document.querySelector(selector);
            if (!list) {
                return false;
            }

            const cards = list.querySelectorAll('article[data-test="JobTile"]');
            return cards.length > 0;
        }
        """,
        arg=JOBS_LIST_SELECTOR,
        timeout=WAIT_TIMEOUT_MS,
    )


def move_mouse_to_locator(page: Page, locator: Locator) -> None:
    box = locator.bounding_box()
    if box is None:
        return

    target_x = box["x"] + (box["width"] / 2)
    target_y = box["y"] + (box["height"] / 2)
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


def get_visible_card_locators(page) -> list[Locator]:
    jobs_list = page.locator(JOBS_LIST_SELECTOR)
    cards = jobs_list.locator(JOB_CARD_SELECTOR)
    visible_cards: list[Locator] = []

    for index in range(cards.count()):
        card = cards.nth(index)
        if card.is_visible():
            visible_cards.append(card)

    return visible_cards


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


def extract_job(card: Locator, query: str, fallback_page: int, fallback_position: int) -> dict:
    title_link = card.locator(TITLE_LINK_SELECTOR)
    title = get_optional_text(title_link)
    relative_job_url = title_link.first.get_attribute("href") if title_link.count() else None
    job_type, budget_or_rate = extract_job_type_and_budget(card)
    page_number = card.get_attribute("data-ev-page_number")
    position = card.get_attribute("data-ev-position")

    return {
        "query": query,
        "page": int(page_number) if page_number and page_number.isdigit() else fallback_page,
        "position": int(position) if position and position.isdigit() else fallback_position,
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


def extract_jobs(page, query: str) -> list[dict]:
    jobs: list[dict] = []
    visible_cards = get_visible_card_locators(page)

    for index, card in enumerate(visible_cards, start=1):
        jobs.append(extract_job(card, query, fallback_page=1, fallback_position=index))

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

    page.wait_for_timeout(int(random_delay(PRE_NEXT_PAGE_DELAY_RANGE) * 1000))
    next_button.scroll_into_view_if_needed()
    expect(next_button).to_be_visible(timeout=WAIT_TIMEOUT_MS)
    move_mouse_to_locator(page, next_button)
    next_button.hover()
    with page.expect_navigation(wait_until="domcontentloaded", timeout=WAIT_TIMEOUT_MS):
        next_button.click()

    page.wait_for_url(expected_url, wait_until="domcontentloaded", timeout=WAIT_TIMEOUT_MS)

    wait_for_list_stability(page)
    page.wait_for_timeout(int(random_delay(POST_LIST_DELAY_RANGE) * 1000))
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


def run(query: str) -> tuple[Path, int]:
    url = build_search_url(query)
    jobs: list[dict] = []

    with Camoufox(headless=False) as browser:
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(int(random_delay(INITIAL_INTERACTION_DELAY_RANGE) * 1000))
        wait_for_jobs_list(page)
        wait_for_list_stability(page)
        page.wait_for_timeout(int(random_delay(POST_LIST_DELAY_RANGE) * 1000))
        jobs.extend(extract_jobs(page, query))

        if not go_to_next_page(page):
            raise SystemExit("Failed to move to the second results page.")

        jobs.extend(extract_jobs(page, query))

    output_path = save_jobs(jobs, Path.cwd() / OUTPUT_DIRECTORY_NAME)
    return output_path, len(jobs)


def main() -> None:
    query, _card_count = parse_args()

    try:
        output_path, job_count = run(query)
    except OSError as exc:
        print(f"Failed to save results: {exc}")
        raise SystemExit(1) from exc

    print(f"Saved {job_count} jobs to {output_path}")


if __name__ == "__main__":
    main()
