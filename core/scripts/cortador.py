from PyPDF2 import PdfReader, PdfWriter

def cortarHolerite(data, holerite): #Função que pega o holerite, o ponto e a data e corta eles
        holerite.seek(0) 
        pdfReader = PdfReader(holerite) #Cria um Objeto de ler PDF
        numPages = len(pdfReader.pages) #Pega a quantidade de páginas
        
        for pageNumber in range(numPages): #Percorre as paginas de acordo com o numero ja pego anteriormente
            pdfWriter = PdfWriter() #Cria um Objeto de escrever PDF
            page = pdfReader.pages[pageNumber] #Pega a pagina atual
            pdfWriter.add_page(page) #Cria uma cópia da pagina atual
            
            with open(f"pagina_{pageNumber + 1}.pdf", "wb") as outputPdf:
                pdfWriter.write(outputPdf) 
    
def cortarPonto(data, ponto): #Função que pega o holerite, o ponto e a data e corta eles
        ponto.seek(0) 
        pdfReader = PdfReader(ponto) #Cria um Objeto de ler PDF
        numPages = len(pdfReader.pages) #Pega a quantidade de páginas
        
        for pageNumber in range(numPages): #Percorre as paginas de acordo com o numero ja pego anteriormente
            pdfWriter = PdfWriter() #Cria um Objeto de escrever PDF
            page = pdfReader.pages[pageNumber] #Pega a pagina atual
            pdfWriter.add_page(page) #Cria uma cópia da pagina atual
            
            with open(f"pagina_{pageNumber + 1}.pdf", "wb") as outputPdf:
                pdfWriter.write(outputPdf)
        
        