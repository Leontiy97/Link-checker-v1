import openpyxl

from parser.link_cheker_v1 import LinkChecker


async def first_script(ref_page, page_link, anchor_text):
    httpx_result = LinkChecker(ref_page, page_link, anchor_text)
    result = await httpx_result.run()
    return result

async def run_from_excel(filepath):
    excel = openpyxl.load_workbook(filepath).active
    headers = {cell.value: index for index, cell in enumerate(excel[1], start=1)}
    col_ref = headers["Ref page"]
    col_anchor = headers["Anchor"]
    col_link = headers["Project url"]
    col_verdict = headers["Verdict"]

    for row in excel.iter_rows(min_row=2, values_only=False):
        ref_page = row[col_ref - 1].value
        anchor = row[col_anchor - 1].value
        page_link = row[col_link - 1].value

        result = await first_script(ref_page, page_link, anchor)
        print(result)
        row[col_verdict-1].value = result.value
