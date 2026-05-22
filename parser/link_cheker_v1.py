from parser.httpx_page import HttpxPage
from parser.verdicts import Verdicts


class LinkChecker:
    def __init__(self, ref_page: str, page_link: str, anchor_text:str):
        self.ref_page = ref_page
        self.page_link = page_link
        self.anchor_text = anchor_text

    async def run(self):
        run_with_httpx = HttpxPage(self.ref_page)
        result = await run_with_httpx.find_link_or_anchor(self.page_link, self.anchor_text)
        return result