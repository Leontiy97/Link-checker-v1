from playwright.async_api import async_playwright
from parser.base_page import BasePage
from parser.captcha_markers import captcha_is_detected
from parser.user_agent import UserAgentPool
from parser.utils import url_normalise, normalise_anchor
from parser.verdicts import Verdicts

class PlaywrightPage(BasePage):
    async def find_link_or_anchor(self, page_link: str, anchor_text: str):
        async with async_playwright() as playwright:
            ua_pool = UserAgentPool().get_random_ua()["User-Agent"]
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context(user_agent=ua_pool, )

            try:
                page = await context.new_page()
                await page.goto(self.ref_page, wait_until="domcontentloaded")
                final_url = page.url

                if captcha_is_detected(await page.content()):
                    return Verdicts.CAPTCHA_BLOCK
                if url_normalise(final_url) != self.ref_page:
                    return Verdicts.REDIRECT_DETECTED

                await page.wait_for_timeout(5000)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                await page.wait_for_timeout(5000)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                normal_page_link = url_normalise(page_link)
                normal_anchor = normalise_anchor(anchor_text)

                try:
                    found_link = False
                    found_anchor = False
                    a_elements = await page.locator('a').all()
                    for element in a_elements:
                        href_link = await element.get_attribute("href")
                        href_anchor = await element.inner_text()
                        if href_link is not None and url_normalise(href_link) == normal_page_link:
                            found_link = True
                            if normalise_anchor(href_anchor) == normal_anchor:
                                return Verdicts.FOUND
                        if normalise_anchor(href_anchor) == normal_anchor:
                            found_anchor = True

                    if found_link:
                        return Verdicts.ANCHOR_MISMATCH
                    elif found_anchor:
                        return Verdicts.LINK_MISMATCH
                    else:
                        return Verdicts.LINK_DELETED

                except Exception as e:
                    if "ERR_CERT" in str(e):
                        print(f"SSL Error in PlaywrightPage: {e}")
                        return Verdicts.SSL_ERROR
                    print(f"Error in PlaywrightPage: {e}")
                    return Verdicts.SERVER_ERROR

            except Exception as e:
                if "ERR_CERT" in str(e):
                    print(f"SSL Error in PlaywrightPage: {e}")
                    return Verdicts.SSL_ERROR
                print(f"Error to load: {e}")
                return Verdicts.NETWORK_ERROR

            finally:
                    await browser.close()
