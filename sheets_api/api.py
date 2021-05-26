from sheets_api import sheet
import os
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def write(_range, data):
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=_range,
                                    valueInputOption="USER_ENTERED", body={"values": data})
    response = request.execute()


def read(_range):
    request = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=_range)
    response = request.execute()
    values = response.get('values', [])
    return values


def clear_last_char(name):
    return ' '.join(name.split())


def check_update(row, new_row):
    is_exist = lambda x: bool(str(x).replace(' ', ''))

    if is_exist(row[1]) and not is_exist(new_row[1]):
        new_row[1] = row[1]

    if is_exist(row[2]) and not is_exist(new_row[2]):
        new_row[2] = row[2]
    elif is_exist(row[2]) and is_exist(new_row[2]):
        new_row[2] = int(new_row[2]) + int(row[2])

    if len(row) == 4 and len(new_row) == 3:
        new_row.append(row[3])
    elif (len(row) == 4 and len(new_row) == 4
          and is_exist(row[3]) and is_exist(new_row[3])):
        new_row[3] = int(new_row[3]) + int(row[3])

    return new_row


def update_row(names, name, location, data):
    index = names.index(name)
    row = read(f"{location.column.name_start}{location.column.start + index}:"
               f"{location.column.name_end}{location.column.start + index}")
    row = check_update(row[0], data[0])
    return [row], index


def update_or_write(location, data):
    names = read(location.range)
    name = [data[0][0]]
    data[0][0] = clear_last_char(name[0])
    name = [data[0][0]]

    if name in names:
        data, index = update_row(names, name, location, data)
    else:
        try:
            index = names.index([])
        except ValueError:
            index = len(names)

    update_range = f"{location.column.name_start}{location.column.start + index}"
    write(update_range, data)

