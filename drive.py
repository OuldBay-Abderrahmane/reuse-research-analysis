import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Define the scope for the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Authenticate using OAuth2."""
    credentials = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(credentials.to_json())

    return credentials

def list_files(service):
    """List all files in Google Drive."""
    results = service.files().list(q="trashed=false",
                                   fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items

def download_file(service, file_name, save_path):
    """Download a file by name from Google Drive."""
    files = list_files(service)
    file_id = None

    for file in files:
        if file['name'] == file_name:
            file_id = file['id']
            break

    if file_id:
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(save_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        print(f'File "{file_name}" downloaded successfully.')
    else:
        print(f'File "{file_name}" not found.')

def main():
    # Authenticate and create a service object
    credentials = authenticate()
    service = build('drive', 'v3', credentials=credentials)

    # Specify the file name to download
    file_name_to_download = 'YourFileName.txt'

    # Specify the path where the file will be saved
    save_path = 'DownloadedFiles/' + file_name_to_download

    # Download the file
    download_file(service, file_name_to_download, save_path)

if __name__ == '__main__':
    main()
