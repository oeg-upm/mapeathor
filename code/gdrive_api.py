from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import configparser
import sys

def get_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        cred_file = config['drive_config']['credentials_path']
        file_id = config['drive_config']['spreadsheet_id']
    except:
        print('ERROR: Config file not valid')
        sys.exit()

    return cred_file, file_id

def download_sheet(config_file):
    scopes = 'https://www.googleapis.com/auth/drive.readonly'
    mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    cred_file, file_id = get_config(config_file)

    store = file.Storage('driveAPI/storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(cred_file, scopes)
        creds = tools.run_flow(flow, store)
    drive = build('drive', 'v3', http=creds.authorize(Http()))

    request = drive.files().export_media(fileId=file_id, mimeType=mimeType)
    result = request.execute()
    with open('../data/drive_sheet.xlsx', 'wb') as f:
        f.write(result)