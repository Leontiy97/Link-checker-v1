import asyncio

from excel_runner import run_from_excel

# Fix ssl error with: pip install pip-system-certs, certifi

filepath = "C:/Users/kbjyt/Desktop/test.xlsx"

asyncio.run(run_from_excel(filepath))
