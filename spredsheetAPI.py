import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.

VALUES_START_ROW = 5

service = None


def initCreds():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    global service
    service = build('sheets', 'v4', credentials=creds)
    return service 



def mergeCells(sheetId, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex, spreadsheetId):
    requests = [
        {
            "mergeCells": {
                "range": {
                    "sheetId": sheetId,
                    "startRowIndex": startRowIndex,
                    "endRowIndex": endRowIndex,
                    "startColumnIndex": startColumnIndex,
                    "endColumnIndex": endColumnIndex
                },
                "mergeType": "MERGE_ALL"
            }
        }
    ]

    body = {
        'requests': requests
    }

    request = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId, body=body) ###Заменить айди, добавить в параметры функции, сделать инициализацию не в мейне а в функции new table
    response = request.execute()


def updateCell(values, range_name, spreadsheetId):
    values = [
        [
            f"{values}"
        ],
    ]

    body = {
        'values': values
    }

    sheet = service.spreadsheets()

    result = sheet.values().update(valueInputOption='USER_ENTERED', spreadsheetId=spreadsheetId,
                                   range=range_name, body=body).execute()


def getFormulaData(range_name, spreadsheetId):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range=range_name, valueRenderOption='FORMULA').execute()
    values = result.get('values', [])

    result = []
    if not values:
        result = []
    else:

        for row in values:
            if (row != []):
                result.append(str(row[0]))
            else:
                break

    return result


def getValueData(range_name, spreadsheetId):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range=range_name).execute()
    values = result.get('values', [])

    result = []
    if not values:
        result = ['']
    else:
        for row in values:
            result.append(row[0])

    return result


def createCellsCouple(current_sheet, name_data, value_data, name_column, value_column, spreadsheetId):
    """found row id for new values"""
    range_name = f'{current_sheet}!{name_column}{VALUES_START_ROW}:{name_column}100'

    respond = getFormulaData(range_name, spreadsheetId)

    current_row_number = VALUES_START_ROW+len(respond)

    updateCell(value_data, f'{current_sheet}!{value_column}{current_row_number}', spreadsheetId)

    updateCell(name_data, f'{current_sheet}!{name_column}{current_row_number}', spreadsheetId)


def getSheetId(sheet_name, spreadsheetId):
    spreadsheet = service.spreadsheets().get(
        spreadsheetId=spreadsheetId).execute()
    sheet_id = None
    for _sheet in spreadsheet['sheets']:
        if _sheet['properties']['title'] == sheet_name:
            sheet_id = _sheet['properties']['sheetId']

    return sheet_id
