from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from parser.base_page import BasePage
from parser.captcha_markers import CaptchaMarkers
from parser.user_agent import UserAgentPool
from parser.verdicts import Verdicts


async def fetch_by_pw(ref_page) -> tuple[str, BeautifulSoup]:
    async with async_playwright() as playwright:
        ua_pool = UserAgentPool().get_random_ua()["User-Agent"]
        browser = None
        try:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=ua_pool)
            page = await context.new_page()
            await page.goto(ref_page, wait_until="domcontentloaded")
            final_url = page.url
            pw_html = str(await page.content())
            html = BeautifulSoup(pw_html, "html.parser")
            return final_url, html
        finally:
            if browser:
                await browser.close()


def captcha_is_detected(html) -> bool:
    html_text = str(html).lower()
    for marker in CaptchaMarkers().take_markers():
        if marker.lower() in html_text:
            return True
    return False


class PlaywrightPage(BasePage):
    async def find_link_or_anchor(self, page_link: str, anchor_text: str):
        try:
            final_url, html = await fetch_by_pw(self.ref_page)
        except Exception as e:
            print(f"Network error: {e}")
            return Verdicts.NETWORK_ERROR

        if final_url != self.ref_page:
            return Verdicts.REDIRECT_DETECTED

        if captcha_is_detected(html):
            return Verdicts.CAPTCHA_BLOCK

        try:
            found_link = False
            found_anchor = False
            for element in html.find_all('a'):
                href_link = element.get('href')
                href_anchor = element.get_text(strip=True)
                if href_link == page_link and href_anchor == anchor_text:
                    return Verdicts.FOUND
                if href_link == page_link:
                    found_link = True
                if href_anchor == anchor_text:
                    found_anchor = True

            if found_link:
                return Verdicts.ANCHOR_MISMATCH
            elif found_anchor:
                return Verdicts.LINK_MISMATCH
            else:
                return Verdicts.LINK_DELETED

        except Exception as e:
            print(f"Error in HttpxPage: {e}")
            return Verdicts.SERVER_ERROR
