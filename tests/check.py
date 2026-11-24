from pathlib import Path

import os
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]

with sync_playwright() as p, TemporaryDirectory() as temp:
    browser = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH"))
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "index.html").as_uri())
    assert "2.25 cups flour" in page.locator("#result").inner_text()
    page.locator("#items").fill("1/0 | cup | flour")
    page.locator("#go").click()
    assert page.locator("#print").is_hidden()
    page.locator("#items").fill("1/2 | tsp | salt")
    page.locator("#go").click()
    assert "0.75 tsp salt" in page.locator("#result").inner_text()
    page.emulate_media(media="print")
    assert page.locator("#items").is_hidden()
    page.emulate_media(media="screen")
    assert not errors, errors
    browser.close()
