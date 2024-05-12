from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

# Set up credentials
credentials = service_account.Credentials.from_service_account_file('D:/Study/Mlops/Mlops-task_Assignment02/default.json')
drive_service = build('drive', 'v3', credentials=credentials)

# File to upload
file_name = 'data.csv'
file_metadata = {'name': file_name}

# Specify the path to your data.csv file
file_path = 'D:/Study/Mlops/Mlops-task_Assignment02/data.csv'

# Upload file
media = MediaFileUpload(file_path, mimetype='text/csv')
file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
print('File ID:', file.get('id'))
