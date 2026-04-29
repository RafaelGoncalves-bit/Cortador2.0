from PyPDF2 import PdfWriter
from io import BytesIO

class Escritor:

    def __init__(self, drive):
        self.drive = drive

    def escrever_pdfs(self, tipo, nome, page, pasta_id):

        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)

        buffer = BytesIO()
        pdf_writer.write(buffer)
        buffer.seek(0)

        if tipo == "holerite":
            nome_arquivo = f"Holerite.pdf"
        elif tipo == "ponto":
            nome_arquivo = f"Espelho Ponto.pdf"
        else:
            nome_arquivo = f"Documento - {nome}.pdf"

        # ENVIA PRO DRIVE
        self.drive.upload_pdf(nome_arquivo, buffer, pasta_id)