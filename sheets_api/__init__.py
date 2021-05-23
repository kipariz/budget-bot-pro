import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from collections import namedtuple
import json

here = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(here, os.pardir))
config_path = os.path.join(root, "google-credentials.json")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None

try:
    with open(config_path) as config_file:
        creds_json = json.load(config_file)
        print(creds_json)

    creds = service_account.Credentials.from_service_account_file(config_path, scopes=SCOPES)
except:
    print("Problem with creds!")


service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()


Finance = namedtuple('Finance', ['income', 'expenses'])
Locations = namedtuple('Locations', ['column', 'range'])
Column = namedtuple('Column', ['name', 'start'])

finance = Finance(Locations(Column('A', 4), 'A4:A100'),
                  Locations(Column('F', 4), 'F4:F100'))

