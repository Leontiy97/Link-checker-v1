import asyncio
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from parser.user_agent import UserAgentPool


async def fetch_by_httpx(ref_page: str) -> BeautifulSoup:
    ua_pool = UserAgentPool()
    async with httpx.AsyncClient(headers=ua_pool.get_random_ua(), follow_redirects=True) as client:
        response = await client.get(ref_page)
        html = BeautifulSoup(response.text, "html.parser")
        print(str(html)[:200])
        return html

async def fetch_by_pw(ref_page):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(ref_page, wait_until="load")
        await page.screenshot(path="screenshot.png")
        await browser.close()


async def first_script(ref_page):
    await fetch_by_httpx(ref_page)
    await fetch_by_pw(ref_page)

test_url = "https://dzen.ru"
asyncio.run(first_script(test_url))