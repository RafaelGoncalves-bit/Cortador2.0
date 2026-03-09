import os
import re
import pdfplumber
from pypdf import PdfReader, PdfWriter

arquivo_pdf = r"C:\Users\rafae\Downloads\holerites.pdf"
pasta_saida = r"C:\Users\rafae\Downloads\Organizados"

os.makedirs(pasta_saida, exist_ok=True)

def extrair_nome(texto):
    linhas = texto.splitlines()[:5]  # só primeiras linhas
    topo = " ".join(linhas)

    padrao = r"\d+\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]+(?:\s+[A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]+){1,3})"
    
    
    match = re.search(padrao, topo)
    if match:
        nome = match.group(1).strip()
        nome = nome[:-2]
        nome = re.sub(r'[\\/*?:"<>|]', "", nome)
        return nome

    return "Sem_Nome"

reader = PdfReader(arquivo_pdf)

with pdfplumber.open(arquivo_pdf) as pdf:
    for i, pagina_pdfplumber in enumerate(pdf.pages):
        texto = pagina_pdfplumber.extract_text() or ""
        nome = extrair_nome(texto)
        

        pasta_nome = os.path.join(pasta_saida, nome)
        os.makedirs(pasta_nome, exist_ok=True)

        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        caminho_saida = os.path.join(pasta_nome, f"pagina_{i+1}.pdf")
        with open(caminho_saida, "wb") as f:
            writer.write(f)

print("Arquivos organizados por nome com sucesso.")