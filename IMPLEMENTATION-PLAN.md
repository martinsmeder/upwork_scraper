# Implementation Plan

- [x] Open browser, wait for manual captcha solve, detect JobsList, close.
- [x] Open browser, detect JobsList, count visible cards, print count, close.
- [ ] Extract all fields from all cards on one page, print JSON to stdout.
- [ ] Save one-page results to jobsN.json.
- [ ] Click next and scrape the second page.
- [ ] Repeat until card count is reached.
- [ ] Add CLI polish, file naming, and error handling.
