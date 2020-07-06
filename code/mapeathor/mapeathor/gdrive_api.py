from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
import configparser
import sys
from os import path

def get_config(config_file):
    """
    Loads the config file 'config_file', gets the spreadsheet id and the credentials file path and returns them
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    # Check the config file exists
    if not path.exists(config_file):
        print('ERROR: Config file cannot be found')
        sys.exit()
    print('Downloading the Google Spreadsheet requested')

    # Check the config file is correct and the data can be retrieved
    try:
        cred_file = config['drive_config']['credentials_path']
        file_id = config['drive_config']['spreadsheet_id']
    except KeyError:
        print('ERROR: Config file not valid')
        sys.exit()
    return cred_file, file_id


def download_sheet(config_file):
    """
    Retrieves the credentials and downloads the requested spreadsheet
    """
    scopes = 'https://www.googleapis.com/auth/drive.readonly'
    mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    cred_file, file_id = get_config(config_file)

    # When it's not the first time, so the authentication in Google doesn't have to be done more than once
    store = file.Storage('driveAPI/storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(cred_file, scopes)
        creds = tools.run_flow(flow, store)

    # Download the file
    drive = build('drive', 'v3', http=creds.authorize(Http()))
    request = drive.files().export_media(fileId=file_id, mimeType=mimeType)
    try:
        result = request.execute()
    except HttpError as err:
        print('ERROR: Something went wrong downloading the requested spreadsheet.')
        print('The error is shown below')
        print(err)
        sys.exit()
    # Write the retrieved file in XLSX format
    with open('../data/drive_sheet.xlsx', 'wb') as f:
        f.write(result)