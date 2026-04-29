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
        creds = None
        token_path = os.path.join(settings.BASE_DIR, 'core/utils/token.json')
        client_secret_path = os.path.join(settings.BASE_DIR, 'core/utils/cliente_secret.json')

        # LER TOKEN COM PROTEÇÃO
        if os.path.exists(token_path):
            try:
                with open(token_path, 'r') as token:
                    info = json.load(token)

                # só usa se tiver refresh_token
                if "refresh_token" in info:
                    creds = Credentials.from_authorized_user_info(info, self.SCOPES)
                else:
                    print("⚠️ Token inválido (sem refresh_token)")
                    creds = None
            except:
                creds = None

        # FLUXO NORMAL
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_path, self.SCOPES
                )

                # FORÇA GERAR refresh_token
                creds = flow.run_local_server(
                    port=8080,
                    prompt='consent',
                    access_type='offline'
                )

            # SALVA TOKEN CORRETO
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return creds

   