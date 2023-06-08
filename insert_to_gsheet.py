from typing import List

import gspread

# note you need to generate this file in the local directory
SA = gspread.service_account(filename='google_service_account.json')


def check_for_headers(worksheet: gspread.Worksheet, headers: List[str]) -> None:
    """
    Check for headers in the worksheet and add them if they do not exist.
    """
    existing_headers = worksheet.row_values(1)
    if existing_headers != headers:
        if not existing_headers:
            worksheet.append_row(headers)
        else:
            raise ValueError("Existing headers do not match the provided data headers.")


def insert_from_dict(sheet_id: str, sheet_name: str, data: dict, client: gspread.Client = SA):
    """
    Insert a single row of data into a Google Sheet using a dictionary where the key is the column name
    and the value is the row value.
    """
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)

    headers = list(data.keys())
    check_for_headers(worksheet, headers)

    worksheet.append_row(list(data.values()))
