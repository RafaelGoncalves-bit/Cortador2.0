from PyPDF2 import PdfReader, PdfWriter
import core.scripts.extrator as extrator

extrator = extrator.ExtrairNomes("")

class Cortador:
    def __init__(self):
        # A classe não necessita de inicialização no momento.
        pass

    def cortar_holerite(self, holerite):
        holerite.seek(0)
        pdf_reader = PdfReader(holerite)
        num_pages = len(pdf_reader.pages)
        dicionarioNomes = {}
        for page_number in range(num_pages):
            pdf_writer = PdfWriter()
            page = pdf_reader.pages[page_number]
            pdf_writer.add_page(page)
            texto = page.extract_text() or ""
            
            nome = extrator.extrair_nome_h(texto)
            dicionarioNomes["nome"] = nome

            with open(f"{nome}.pdf", "wb") as outputPdf:
                pdf_writer.write(outputPdf)


            print(dicionarioNomes)
        
    def cortar_ponto(self, ponto):
        ponto.seek(0)
        pdf_reader = PdfReader(ponto)
        num_pages = len(pdf_reader.pages)

        for page_number in range(num_pages):
            pdf_writer = PdfWriter()
            page = pdf_reader.pages[page_number]
            pdf_writer.add_page(page)

            texto = page.extract_text() or ""
            nome = extrator.extrair_nome_p(texto)

            with open(f"{nome}.pdf", "wb") as outputPdf:
                pdf_writer.write(outputPdf)

            print(nome)