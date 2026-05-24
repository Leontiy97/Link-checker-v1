import os

import certifi
from playwright.async_api import async_playwright, Page, Browser, Playwright
from parser.base_page import BasePage
from parser.captcha_markers import captcha_is_detected
from parser.user_agent import UserAgentPool
from parser.utils import url_normalise
from parser.verdicts import Verdicts


async def fetch_by_pw(ref_page) -> tuple[Playwright, Browser, str, Page]:
    os.environ["SSL_CERT_FILE"] = certifi.where()
    playwright = await async_playwright().start()
    ua_pool = UserAgentPool().get_random_ua()["User-Agent"]
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(user_agent=ua_pool, )
    page = await context.new_page()
    await page.goto(ref_page, wait_until="domcontentloaded")
    final_url = page.url
    return playwright, browser, final_url, page


class PlaywrightPage(BasePage):
    async def find_link_or_anchor(self, page_link: str, anchor_text: str):
        playwright = None
        browser = None
        try:
            playwright, browser, final_url, page = await fetch_by_pw(self.ref_page)
        except Exception as e:
            print(f"Network error: {e}")
            return Verdicts.NETWORK_ERROR

        if url_normalise(final_url) != self.ref_page:
            return Verdicts.REDIRECT_DETECTED

        if captcha_is_detected(await page.content()):
            return Verdicts.CAPTCHA_BLOCK
        await page.wait_for_timeout(5000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await page.wait_for_timeout(5000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        normal_page_link = url_normalise(page_link)
        try:
            found_link = False
            found_anchor = False
            a_elements = await page.locator('a').all()
            for element in a_elements:
                href_link = await element.get_attribute("href")
                href_anchor = await element.inner_text()
                if href_link is not None and url_normalise(href_link) == normal_page_link:
                    found_link = True
                    if href_anchor == anchor_text:
                        return Verdicts.FOUND
                if href_anchor == anchor_text:
                    found_anchor = True

            if found_link:
                return Verdicts.ANCHOR_MISMATCH
            elif found_anchor:
                return Verdicts.LINK_MISMATCH
            else:
                return Verdicts.LINK_DELETED

        except Exception as e:
            print(f"Error in PlaywrightPage: {e}")
            return Verdicts.SERVER_ERROR
        finally:
            if browser:
                await browser.close()
            if playwright:
                await playwright.stop()
