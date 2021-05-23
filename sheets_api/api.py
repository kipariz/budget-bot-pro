from sheets_api import sheet
import os
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# def get_first_sheet_title(_sheet):
#     """As I understand by default, if name of sheet is not passed, first sheet will be used.
#     Hence this function is not needed right now, but could be useful later.
#     """
#     sheet_metadata = _sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
#     sheets = sheet_metadata.get('sheets', '')
#     title = sheets[0].get("properties", {}).get("title", "Sheet1")
#     return title


def write(_range, data):
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=_range,
                                    valueInputOption="USER_ENTERED", body={"values": data})
    response = request.execute()


def read(_range):
    request = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=_range)
    response = request.execute()
    values = response.get('values', [])
    return values


def update_or_write(location, data):
    names = read(location.range)
    name = [data[0][0]]
    try:
        index = names.index(name)

    except ValueError:
        try:
            index = names.index([])
        except ValueError:
            index = len(names)

    update_range = f"{location.column.name}{location.column.start + index}"
    write(update_range, data)

