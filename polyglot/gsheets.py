import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from openai import OpenAI
from langdetect import detect

client = OpenAI()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1NnavVJiVF3QySSG_Sb-m28AHUBB8LtjHt_FOpSSssn8"
RANGE_NAME = "Sheet1!A:B"


def authenticate_google():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def read_data_from_sheets(creds, spreadsheet_id, select_range):
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range=select_range)
        .execute()
    )
    values = result.get("values", [])
    # Check if values is not empty and remove the first row
    if values:
        values = values[1:]

    return values

def write_data_to_sheets(creds, spreadsheet_id, select_range, data):
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    body = {
        'values': data
    }
    result = sheet.values().update(
        spreadsheetId=spreadsheet_id, range=select_range,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def print_output(values):
    if not values:
        print("No data found.")
    else:
        for row in values:
            print(f"{row[0]}, {row[1]}")

def detect_language(question):
    detected_language = detect(question)

    return detected_language

def translate_to_english(text_to_translate):

    response = client.chat.completions.create(
        model="gpt-4",
        temperature=1,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to identify language and translate it to English."
            },
            {
                "role": "user",
                "content": f"Translate the following text to English. Only respond with the translated text as a string and nothing else: '{text_to_translate}'"

            }
        ]
    )
    english_translation = response.choices[0].message.content

    return english_translation

def main():
    try:
        creds = authenticate_google()
        values = read_data_from_sheets(creds, SPREADSHEET_ID, RANGE_NAME )
        translations = []
        
        for row in values:
            language = detect_language(row[1])
            print(f"{row[0]}, {row[1]}", language)
            if language != 'en':
                translation = translate_to_english(row[1])
                translations.append([translation])
            else:
                translations.append(["English"])

        write_data_to_sheets(creds, SPREADSHEET_ID, "Sheet1!C2:C", translations)


    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()