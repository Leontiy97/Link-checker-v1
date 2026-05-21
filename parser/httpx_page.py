import httpx
from bs4 import BeautifulSoup

from parser.base_page import BasePage
from parser.user_agent import UserAgentPool
from parser.verdicts import Verdicts


class HttpxPage(BasePage):
    async def find_link_or_anchor(self, page_link: str, anchor_text: str, ):
        final_url, html = await fetch_by_httpx(self.ref_page)
        if final_url != self.ref_page:
            return Verdicts.REDIRECT_DETECTED
        try:
            for link, text in html.findAll('a'):
                if link.get('href') == page_link and text.get_text(strip=True) == anchor_text:
                    return Verdicts.FOUND
                elif link.get('href') == page_link:
                    return Verdicts.ANCHOR_MISMATCH
                elif text.get_text(strip=True) == anchor_text:
                    return Verdicts.LINK_MISMATCH
        except Exception:
            pass

async def fetch_by_httpx(ref_page: str) -> [str, BeautifulSoup]:
    ua_pool = UserAgentPool()
    async with httpx.AsyncClient(headers=ua_pool.get_random_ua(), follow_redirects=True) as client:
        response = await client.get(ref_page)
        final_url = response.url
        html = BeautifulSoup(response.text, "html.parser")
        return final_url, html

