from parser.utils import url_normalise
from parser.verdicts import Verdicts


class BasePage:
    def __init__(self, ref_page: str):
        self.ref_page = url_normalise(ref_page)

    async def find_link_or_anchor(self, page_link: str, anchor_text: str) -> Verdicts:
        raise NotImplementedError