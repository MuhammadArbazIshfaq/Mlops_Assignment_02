from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up credentials
credentials = service_account.Credentials.from_service_account_file('D:/Study/Mlops/Mlops-task_Assignment02/default.json')
drive_service = build('drive', 'v3', credentials=credentials)

# List files
results = drive_service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(f"{item['name']} ({item['id']})")
