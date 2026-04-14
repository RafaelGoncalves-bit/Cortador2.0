from PyPDF2 import PdfReader, PdfWriter
import re

def extrairNomeH(texto):
    linhas = texto.split('\n')

    for linha in linhas:
        if "/" in linha:
            partes = linha.strip().split()

            for i, parte in enumerate(partes):
                if parte.isdigit():
                    return " ".join(partes[i+1:])

    return ""

def extrairNomeP(texto):
    linhas = texto.split('\n')

    for linha in linhas:
        linha = linha.strip()

        if re.match(r'^[A-ZÀ-Ÿ\s]{5,}$', linha):
            if "EMPRESA" not in linha and "DEPARTAMENTO" not in linha:
                return linha

    return ""

def cortarHolerite(holerite):
    holerite.seek(0)
    pdfReader = PdfReader(holerite)
    numPages = len(pdfReader.pages)

    for pageNumber in range(numPages):
        pdfWriter = PdfWriter()
        page = pdfReader.pages[pageNumber]
        pdfWriter.add_page(page)

        with open(f"pagina_{pageNumber + 1}.pdf", "wb") as outputPdf:
            pdfWriter.write(outputPdf)

        texto = page.extract_text() or ""
        nome = extrairNomeH(texto)

        print(nome)
    
def cortarPonto(ponto):
    ponto.seek(0)
    pdfReader = PdfReader(ponto)
    numPages = len(pdfReader.pages)

    for pageNumber in range(numPages):
        pdfWriter = PdfWriter()
        page = pdfReader.pages[pageNumber]
        pdfWriter.add_page(page)

        texto = page.extract_text() or ""
        nome = extrairNomeP(texto)

        with open(f"{nome}_pagina_{pageNumber + 1}.pdf", "wb") as outputPdf:
            pdfWriter.write(outputPdf)

        print(nome)