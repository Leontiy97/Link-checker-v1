import httpx
from bs4 import BeautifulSoup
from httpx import NetworkError

from parser.base_page import BasePage
from parser.captcha_markers import CaptchaMarkers, captcha_is_detected
from parser.user_agent import UserAgentPool
from parser.utils import url_normalise, normalise_anchor
from parser.verdicts import Verdicts

async def fetch_by_httpx(ref_page: str) -> tuple[str, BeautifulSoup]:
    ua_pool = UserAgentPool()
    async with httpx.AsyncClient(headers=ua_pool.get_random_ua(), follow_redirects=True) as client:
        response = await client.get(ref_page)
        final_url = str(response.url)
        html = BeautifulSoup(response.text, "html.parser")
        return final_url, html

class HttpxPage(BasePage):
    async def find_link_or_anchor(self, page_link: str, anchor_text: str):
        try:
            final_url, html = await fetch_by_httpx(self.ref_page)
        except httpx.ConnectError as e:
            if "SSL" in str(e):
                print(f"SSL error: {e}")
            else:
                print(f"Other connection error: {e}")
            return Verdicts.NETWORK_ERROR
        except NetworkError as e:
            print(f"Network error: {e}")
            return Verdicts.NETWORK_ERROR
        except Exception as e:
            print(f"Unexpected error in HttpxPage: {type(e).__name__}: {e}")
            return Verdicts.FALLBACK_NEEDED

        if captcha_is_detected(html):
            return Verdicts.CAPTCHA_BLOCK
        if url_normalise(final_url) != self.ref_page:
            return Verdicts.REDIRECT_DETECTED

        normal_page_link = url_normalise(page_link)
        normal_anchor = normalise_anchor(anchor_text)
        try:
            found_link = False
            found_anchor = False
            for element in html.find_all('a'):
                href_link = element.get('href')
                href_anchor = element.get_text(strip=True)
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
                return Verdicts.FALLBACK_NEEDED

        except Exception as e:
            print(f"Error in HttpxPage: {e}")
            return Verdicts.FALLBACK_NEEDED



