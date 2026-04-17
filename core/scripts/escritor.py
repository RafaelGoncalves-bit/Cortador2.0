from PyPDF2 import PdfWriter
from core.scripts.leitor import LeitorPdfs

class Escritor:
    def __init__(self):
        # A classe não necessita de inicialização no momento.
        pass

    def escrever_pdfs(self, tipo, nome, page):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)
        
        if tipo == "holerite":
            with open("Holerite.pdf", "wb") as outputPdf:
                pdf_writer.write(outputPdf)
        elif tipo == "ponto":
            with open("Espelho Ponto.pdf", "wb") as outputPdf:
                pdf_writer.write(outputPdf)
