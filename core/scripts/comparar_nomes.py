class Comparador:

    def __init__(self, funcionarios):
        self.funcionarios = funcionarios

    def normalizar(self, nome):
        return str(nome).strip().lower()
    
    def extrair_id_pasta(self, link):
        if not link:
            return None
        if "folders/" in link:
            return link.split("folders/")[1].split("?")[0]
        return link

    def comparar(self, resultados):

        # 🔥 agora guarda o funcionario completo
        mapa_funcionarios = {
            self.normalizar(f["nome"]): f
            for f in self.funcionarios
        }

        lista_final = []

        for item in resultados:
            nome_original = item.get("nome", "")
            nome = self.normalizar(nome_original)

            funcionario = mapa_funcionarios.get(nome)

            print("DEBUG nome PDF:", nome_original)
            print("DEBUG funcionario encontrado:", funcionario)

            if funcionario:
                lista_final.append({
                    **item,
                    "pasta_id": self.extrair_id_pasta(funcionario.get("link")),
                    "link": funcionario.get("link"),
                    "linha": funcionario.get("linha"),
                    "email": funcionario.get("email"),
                    "empresa": funcionario.get("empresa"),
                    "status": "encontrado"
                })
            else:
                lista_final.append({
                    **item,
                    "pasta_id": None,
                    "link": "",
                    "linha": None,
                    "email": "",
                    "empresa": "",
                    "status": "não encontrado"
                })

        return lista_final