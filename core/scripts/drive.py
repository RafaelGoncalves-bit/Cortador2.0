import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from django.conf import settings

class GoogleDrive:
    def __init__(self):
        # Escopo para acesso total ao Drive
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = self._autenticar()
        self.service = build('drive', 'v3', credentials=self.creds)

    def _autenticar(self):
        creds = None
        # O arquivo token.json armazena o acesso do usuário
        token_path = os.path.join(settings.BASE_DIR, 'core/utils/token.json')
        client_secret_path = os.path.join(settings.BASE_DIR, 'core/utils/client_secret.json')

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        
        # Se não houver credenciais válidas, faz o login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_path, self.SCOPES)
                # No servidor/Django, isso abrirá uma URL para você clicar e logar
                creds = flow.run_local_server(port=8080)
            
            # Salva o token para a próxima vez
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def criar_pasta(self, nome_pasta, parent_id):
        """
        Verifica se a pasta já existe no diretório pai. 
        Se existir, retorna o ID dela. Se não, cria uma nova.
        """
        nome_pasta = str(nome_pasta).strip()
        
        # 1. Tenta buscar se a pasta já existe
        query = (f"name = '{nome_pasta}' and '{parent_id}' in parents "
                 f"and mimeType = 'application/vnd.google-apps.folder' "
                 f"and trashed = false")
        
        response = self.service.files().list(
            q=query,
            fields="files(id)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        arquivos_existentes = response.get('files', [])

        if arquivos_existentes:
            print(f"Pasta '{nome_pasta}' já existe. Usando ID: {arquivos_existentes[0]['id']}")
            return arquivos_existentes[0]['id']

        # 2. Se não existir, cria a pasta (Lógica do antigo criar_pasta)
        file_metadata = {
            'name': nome_pasta,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else []
        }

        nova_pasta = self.service.files().create(
            body=file_metadata,
            fields='id',
            supportsAllDrives=True
        ).execute()

        print(f"Nova pasta '{nome_pasta}' criada com sucesso! ID: {nova_pasta.get('id')}")
        return nova_pasta.get('id')
    
    def upload_pdf(self, nome_arquivo, arquivo_bytes, parent_id):
        file_metadata = {
            'name': nome_arquivo,
            'parents': [parent_id]
        }

        media = MediaIoBaseUpload(
            arquivo_bytes,
            mimetype='application/pdf',
            resumable=True
        )

        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"Sucesso! Arquivo enviado por VOCÊ. ID: {file.get('id')}")
        return file.get('id')