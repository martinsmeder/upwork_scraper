import random
import sys
from urllib.parse import quote_plus

from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

JOBS_LIST_SELECTOR = 'section[data-test="JobsList"]'
JOB_CARD_SELECTOR = 'article[data-test="JobTile"]'
DEFAULT_QUERY = "mcp"
DEFAULT_CARD_COUNT = 10
INITIAL_INTERACTION_DELAY_RANGE = (2.0, 5.0)
POST_LIST_DELAY_RANGE = (1.0, 3.0)
WAIT_TIMEOUT_MS = 5 * 60 * 1000


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


def count_visible_cards(page) -> int:
    jobs_list = page.locator(JOBS_LIST_SELECTOR)
    cards = jobs_list.locator(JOB_CARD_SELECTOR)
    visible_count = 0

    for index in range(cards.count()):
        if cards.nth(index).is_visible():
            visible_count += 1

    return visible_count


def run(query: str) -> None:
    url = build_search_url(query)

    with Camoufox(headless=False) as browser:
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(int(random_delay(INITIAL_INTERACTION_DELAY_RANGE) * 1000))
        wait_for_jobs_list(page)
        page.wait_for_timeout(int(random_delay(POST_LIST_DELAY_RANGE) * 1000))
        print(count_visible_cards(page))


def main() -> None:
    query, _card_count = parse_args()
    run(query)


if __name__ == "__main__":
    main()
