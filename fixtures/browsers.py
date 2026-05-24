from playwright.async_api import Playwright, Page


from parser.user_agent import UserAgentPool


async def chromium_page_with_state(playwright: Playwright) -> Page:
    ua_pool = UserAgentPool().get_random_ua()["User-Agent"]
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(user_agent=ua_pool)
    yield context.new_page()
    await browser.close()