import time

import openpyxl

from parser.link_cheker_v1 import LinkChecker


async def first_script(ref_page, page_link, anchor_text):
    httpx_result = LinkChecker(ref_page, page_link, anchor_text)
    result = await httpx_result.run()
    return result

async def run_from_excel(filepath):
    start = time.perf_counter()
    excel = openpyxl.load_workbook(filepath)
    excel_sheet = excel.active
    headers = {cell.value: index for index, cell in enumerate(excel_sheet[1], start=1)}
    col_ref = headers["Ref page"]
    col_anchor = headers["Anchor"]
    col_link = headers["Project url"]
    col_verdict = headers["Verdict"]

    for row in excel_sheet.iter_rows(min_row=2, values_only=False):
        ref_page = row[col_ref - 1].value
        anchor = row[col_anchor - 1].value
        page_link = row[col_link - 1].value

        result = await first_script(ref_page, page_link, anchor)
        print(result)
        row[col_verdict-1].value = result.value
    excel.save(filepath)
    end = time.perf_counter()
    total_seconds = end - start
    minutes, seconds = divmod(total_seconds, 60)
    print(f"Total run time: {int(minutes)} min {seconds:.2f} sec")
