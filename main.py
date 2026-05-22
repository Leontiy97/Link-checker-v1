import asyncio
from playwright.async_api import async_playwright

from parser.link_cheker_v1 import LinkChecker

async def fetch_by_pw(ref_page):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(ref_page, wait_until="load")
        await page.screenshot(path="screenshot.png")
        await browser.close()


async def first_script(ref_page, page_link, anchor_text):
    httpx_result = LinkChecker(ref_page, page_link, anchor_text)
    result = await httpx_result.run()
    print(result)
    await fetch_by_pw(ref_page)

test_url = "https://parsemachine.com/sandbox/"
test_link = "/order/"
test_anchor = "Заказать парсинг"
asyncio.run(first_script(test_url, test_link, test_anchor))