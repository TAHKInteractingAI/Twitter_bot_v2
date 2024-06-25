import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1jrXQqjYhBj6k1ufmkWIeIaW6eldB9CF-HDU1K2a1X1M"


def main():
    credentials = None
    range_name = "'500+ Connection'"
    # range_name = "tweet"
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file(
            "token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credential.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets().values()
        result = sheets.get(spreadsheetId=SPREADSHEET_ID,
                            range=range_name).execute()
        values = result.get("values", [])
        url_list = []
        for index, row in enumerate(values):
            if (index != 0):
                url_list.append(row[0])
        print(url_list)
    except HttpError as e:
        print(e)


if __name__ == "__main__":
    main()
