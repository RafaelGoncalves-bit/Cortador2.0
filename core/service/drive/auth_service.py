import os
import json
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class AuthDrive:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        

    # =============================
    # AUTENTICAÇÃO
    # =============================
    def _autenticar(self):
        token_path = os.path.join(settings.BASE_DIR, 'core/utils/token.json')

        if not os.path.exists(token_path):
            raise Exception("Usuário não autenticado. Faça login com Google.")

        creds = Credentials.from_authorized_user_file(
            token_path,
            self.SCOPES
        )

        # renova automaticamente se expirar
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # salva atualizado
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return creds

   