import re

class ExtrairNomes:
    
    def __init__(self, nome):
        self.nome = nome
    
    def extrair_nome_h(self, texto):
        if not texto:
            return ""

        texto = texto.replace("\n", " ")

        # pega tudo que parece nome (2+ palavras maiúsculas)
        candidatos = re.findall(r'\b[A-ZÀ-Ÿ]{2,}(?:\s+[A-ZÀ-Ÿ]{2,}){1,5}\b', texto)

        nomes_validos = []

        for nome in candidatos:
            nome = self.limpar_nome(nome)

            if self.nome_valido(nome):
                nomes_validos.append(nome)

        if not nomes_validos:
            return ""

        # retorna o maior nome (geralmente o completo)
        return max(nomes_validos, key=len)
    
    def limpar_nome(self, nome):
        cortes = [
            " ANALISTA", " AUXILIAR", " ASSISTENTE",
            " AGENTE", " GERENTE", " COORDENADOR",
            " SUPERVISOR", " VENDEDOR"
        ]

        for corte in cortes:
            if corte in nome:
                nome = nome.split(corte)[0]

        return nome.strip()
    
    def nome_valido(self, nome):
        termos_invalidos = [
            "LTDA", "EMPRESA", "CNPJ", "RUA",
            "RECIBO", "SALARIO", "PAGAMENTO",
            "FINANCEIRAS", "AGILLE",
            "CAPITAL", "NEGOCIOS", "INTERMEDIACAO",
            "CONDESSA", "ALVARES", "PENTEADO",  # 🔥 ESSA LINHA resolve seu problema
            "ARARAS", "SP"
        ]

        if len(nome.split()) < 2:
            return False

        if any(t in nome for t in termos_invalidos):
            return False

        return True
    
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