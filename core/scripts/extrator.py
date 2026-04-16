import re

class ExtrairNomes:
    
    def __init__(self, nome):
        self.nome = nome
    
    def extrair_nome_h(self, texto):
        linhas = texto.split('\n')
        
        if not texto:
            return ""

        for linha in linhas:
            if "/" in linha:
                partes = linha.strip().split()

                for i, parte in enumerate(partes):
                    if parte.isdigit():
                        return " ".join(partes[i+1:])

        return ""
    
    def extrair_nome_p(self, texto):
        if not texto:
            return ""

        linhas = texto.split('\n')

        for linha in linhas:
            linha = linha.strip()

            if not linha:
                continue

            if re.match(r'^[A-ZÀ-Ÿ\s]+$', linha) and len(linha) >= 5:
                if "EMPRESA" not in linha and "DEPARTAMENTO" not in linha:
                    return linha.strip()

        return ""