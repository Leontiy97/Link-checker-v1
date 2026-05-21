from playwright.async_api import Page


class BasePage:
    def __init__(self, ref_page: Page):
        self.page = ref_page

    def find_link_or_anchor(self, anchor_text: str):
        ...