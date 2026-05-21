class BasePage:
    def __init__(self, ref_page: str):
        self.ref_page = ref_page

    def find_link_or_anchor(self, page_link: str, anchor_text: str):
        ...