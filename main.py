import asyncio
from playwright.async_api import async_playwright

from parser.link_cheker_v1 import LinkChecker


async def first_script(ref_page, page_link, anchor_text):
    httpx_result = LinkChecker(ref_page, page_link, anchor_text)
    result = await httpx_result.run()
    print(result)


asyncio.run(first_script(test_url, test_link, test_anchor))
asyncio.run(first_script(test_url_1, test_link_1, test_anchor_1))