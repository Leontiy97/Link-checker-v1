from parser.verdicts import Verdicts


class LinkChecker:
    def __init__(self, ref_page: str, page_link: str, anchor_text:str):
        self.ref_page = ref_page
        self.page_link = page_link
        self.anchor_text = anchor_text

    def run(self):
        return