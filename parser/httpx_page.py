import httpx
from bs4 import BeautifulSoup
from httpx import URL, NetworkError

from parser.base_page import BasePage
from parser.captcha_markers import CaptchaMarkers
from parser.user_agent import UserAgentPool
from parser.verdicts import Verdicts

async def fetch_by_httpx(ref_page: str) -> tuple[URL, BeautifulSoup]:
    ua_pool = UserAgentPool()
    async with httpx.AsyncClient(headers=ua_pool.get_random_ua(), follow_redirects=True) as client:
        response = await client.get(ref_page)
        final_url = response.url
        html = BeautifulSoup(response.text, "html.parser")
        return final_url, html

def captcha_is_detected(html) -> bool:
    html_text = str(html).lower()
    for marker in CaptchaMarkers().take_markers():
        if marker.lower() in html_text:
            return True
    return False

class HttpxPage(BasePage):
    async def find_link_or_anchor(self, page_link: str, anchor_text: str):
        try:
            final_url, html = await fetch_by_httpx(self.ref_page)
        except NetworkError as e:
            print(f"Network error: {e}")
            return Verdicts.NETWORK_ERROR
        except Exception as e:
            print(f"Unexpected error in HttpxPage: {e}")
            return Verdicts.FALLBACK_NEEDED

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
                return Verdicts.FALLBACK_NEEDED

        except Exception as e:
            print(f"Error in HttpxPage: {e}")
            return Verdicts.FALLBACK_NEEDED



