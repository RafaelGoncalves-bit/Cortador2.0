from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleDrive:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        self.creds = service_account.Credentials.from_service_account_file(
            '../utils/credentials.json',
            scopes=SCOPES
        )
        
        self.service = build('drive', 'v3', credentials=self.creds)
        
    def criar_pasta(self, nome_pasta, parent_id=None):
        file_metadata = {
            'name': nome_pasta,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        pasta = self.service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()

        print(f"Pasta criada! ID: {pasta.get('id')}")
        return pasta.get('id')