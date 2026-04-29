from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from core.service.drive.auth_service import AuthDrive

class Drive:
    
    def __init__(self):
        self.auth = AuthDrive()
        self.creds = self.auth._autenticar()
        self.service = build('drive', 'v3', credentials=self.creds)
 # =============================
    # CRIAR OU BUSCAR PASTA
    # =============================
    def criar_ou_buscar_pasta(self, nome_pasta, parent_id):
        nome_pasta = str(nome_pasta).strip()

        query = (
            f"name = '{nome_pasta}' and '{parent_id}' in parents "
            f"and mimeType = 'application/vnd.google-apps.folder' "
            f"and trashed = false"
        )

        response = self.service.files().list(
            q=query,
            fields="files(id)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        arquivos = response.get('files', [])

        if arquivos:
            return arquivos[0]['id']

        file_metadata = {
            'name': nome_pasta,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }

        pasta = self.service.files().create(
            body=file_metadata,
            fields='id',
            supportsAllDrives=True
        ).execute()

        print(f"📁 Pasta criada: {nome_pasta}")
        return pasta.get('id')

    # =============================
    # EXTRAIR ID DO LINK
    # =============================
    def extrair_id_pasta(self, link):
        if not link:
            return None

        if "folders/" in link:
            return link.split("folders/")[1].split("?")[0]

        return link

    # =============================
    # VERIFICAR SE ARQUIVO EXISTE
    # =============================
    def arquivo_existe(self, nome_arquivo, parent_id):
        query = (
            f"name = '{nome_arquivo}' and '{parent_id}' in parents "
            f"and trashed = false"
        )

        response = self.service.files().list(
            q=query,
            fields="files(id)"
        ).execute()

        return len(response.get("files", [])) > 0

    # =============================
    # UPLOAD PDF
    # =============================
    def upload_pdf(self, nome_arquivo, arquivo_bytes, parent_id):
        if self.arquivo_existe(nome_arquivo, parent_id):
            print(f"⚠️ Arquivo já existe: {nome_arquivo}")
            return None

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

        print(f"✅ Upload feito: {nome_arquivo}")
        return file.get('id')

    # =============================
    # 🚀 PROCESSAMENTO COMPLETO
    # =============================
    def processar_funcionarios(self, funcionarios, pasta_raiz_id, mes_ano):

        resultado = []

        for f in funcionarios:
            nome = f.get("nome", "").strip()
            link = f.get("link", "")
            holerite = f.get("holerite")
            ponto = f.get("ponto")

            pasta_funcionario_id = self.extrair_id_pasta(link)

            if not pasta_funcionario_id:
                pasta_funcionario_id = self.criar_ou_buscar_pasta(
                    nome,
                    pasta_raiz_id
                )

            pasta_mes_id = self.criar_ou_buscar_pasta(
                mes_ano,
                pasta_funcionario_id
            )

            if holerite:
                self.upload_pdf(
                    f"Holerite_{mes_ano}.pdf",
                    holerite,
                    pasta_mes_id
                )

            if ponto:
                self.upload_pdf(
                    f"Ponto_{mes_ano}.pdf",
                    ponto,
                    pasta_mes_id
                )

            resultado.append({
                "nome": nome,
                "pasta_funcionario": pasta_funcionario_id,
                "pasta_mes": pasta_mes_id,
                "link": f"https://drive.google.com/drive/folders/{pasta_funcionario_id}"
            })

        return resultado