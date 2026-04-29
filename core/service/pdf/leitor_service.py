from PyPDF2 import PdfReader
import core.service.pdf.extrator_service as extrator_service

extrair = extrator_service.ExtrairNomes("")

class LeitorPdfs:

    def ler_pdfs(self, tipo, pdf):
        pdf.seek(0)
        pdf_reader = PdfReader(pdf)
        resultados = []

        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            texto = page.extract_text() or ""
            
            if tipo == "holerite":
                nome = extrair.extrair_nome_h(texto)
            elif tipo == "ponto":
                nome = extrair.extrair_nome_p(texto)

            resultados.append({
                "nome": nome,
                "page": page,
                "tipo": tipo
            })
            

        return resultados