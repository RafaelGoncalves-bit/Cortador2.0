import smtplib
from email.message import EmailMessage
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Credenciais
EMAIL_AGILLE = ""
SENHA_AGILLE = ""
EMAIL_MELO = "contato@melo.com.br"
SENHA_MELO = "sua_senha_aqui"

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def criar_subpasta_no_drive(link_pai, data_raw):
    try:
        # Formata a data para garantir que seja mes-ano (troca / por - se o usuário digitar errado)
        nome_pasta = data_raw.replace("/", "-").strip()

        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        # Extração robusta do ID da pasta
        if "folders/" in link_pai:
            parent_id = link_pai.split("folders/")[1].split("?")[0].split("/")[0]
        else:
            return None, "Link do Drive não contém um ID de pasta válido."

        file_metadata = {
            'name': nome_pasta,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        
        print(f"Tentando criar pasta '{nome_pasta}' dentro do ID: {parent_id}")
        nova_pasta = service.files().create(body=file_metadata, fields='id, webViewLink').execute()
        return nova_pasta.get('webViewLink'), None

    except Exception as e:
        print(f"Erro detalhado no Drive: {e}")
        return None, str(e)

def enviarEmail(empresa_alvo, destino_email, nome_colaborador, link_drive, data_pasta):
    empresa_limpa = str(empresa_alvo).lower().strip()
    remetente = EMAIL_AGILLE if empresa_limpa == "agille" else EMAIL_MELO
    senha = SENHA_AGILLE if empresa_limpa == "agille" else SENHA_MELO

    # Chamada para criar a pasta com o formato mes-ano
    novo_link, erro_drive = criar_subpasta_no_drive(link_drive, data_pasta)
    
    # Se criou a pasta, usa o link novo. Se não, avisa no terminal e usa o original.
    if novo_link:
        link_final = novo_link
        status_pasta = "Pasta criada com sucesso."
    else:
        link_final = link_drive
        status_pasta = f"FALHA ao criar pasta: {erro_drive}"
    
    print(f"Status para {nome_colaborador}: {status_pasta}")

    msg = EmailMessage()
    msg['Subject'] = f"Acesso Drive - {data_pasta.replace('/', '-')} - {nome_colaborador}"
    msg['From'] = remetente
    msg['To'] = destino_email
    
    corpo = (
        f"Olá {nome_colaborador},\n\n"
        f"Sua pasta referente a {data_pasta.replace('/', '-')} foi gerada.\n"
        f"Acesse aqui: {link_final}\n\n"
        f"Atenciosamente,\nEquipe de TI"
    )
    msg.set_content(corpo, charset='utf-8')

    try:
        with smtplib.SMTP_SSL('email-ssl.com.br', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
            return True
    except Exception as e:
        print(f"Erro SMTP: {e}")
        return False