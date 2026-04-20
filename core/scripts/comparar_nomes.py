class Comparador:

    def __init__(self, funcionarios):
        self.funcionarios = funcionarios

    def normalizar(self, nome):
        return nome.strip().lower()
    
    def extrair_id_pasta(self, link):
        if "folders/" in link:
            return link.split("folders/")[1].split("?")[0]
        return link

    def comparar(self, resultados):

        mapa_pastas = {
            self.normalizar(p["nome"]): self.extrair_id_pasta(p["link"])
            for p in self.funcionarios
        }

        lista_final = []

        for item in resultados:
            nome_original = item.get("nome")
            nome = self.normalizar(nome_original)

            if nome in mapa_pastas:
                lista_final.append({
                    **item,
                    "pasta_id": mapa_pastas[nome],
                    "status": "encontrado"
                })
            else:
                lista_final.append({
                    **item,
                    "pasta_id": None,
                    "status": "não encontrado"
                })

        return lista_final