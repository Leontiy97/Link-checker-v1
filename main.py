import asyncio
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def fetch_by_httpx(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        response = await client.get(url)
        html = BeautifulSoup(response.text, "html.parser")
        print(str(html)[:200])
        return

async def fetch_by_pw(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="load")
        await page.screenshot(path="screenshot.png")


async def first_script(url):
    await  fetch_by_httpx(url)
    await fetch_by_pw(url)


asyncio.run(first_script("https://dzen.ru"))