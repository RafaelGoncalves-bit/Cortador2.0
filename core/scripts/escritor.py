from PyPDF2 import PdfWriter
from core.scripts.leitor import LeitorPdfs

class Escritor:
    def __init__(self):
        # A classe não necessita de inicialização no momento.
        pass

    def escrever_pdfs(self, nome, page):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)

        with open(f"{nome}.pdf", "wb") as outputPdf:
            pdf_writer.write(outputPdf)
