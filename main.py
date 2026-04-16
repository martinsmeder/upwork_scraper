from camoufox.sync_api import Camoufox

with Camoufox() as browser:
    page = browser.new_page()
    page.goto("https://www.upwork.com/nx/search/jobs?q=mcp")