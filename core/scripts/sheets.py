import gspread
import pandas as pd
import os
from django.conf import settings

class BuscarFuncionarios:
    def __init__(self):

        caminho_credenciais = os.path.join(
            settings.BASE_DIR,
            'core',
            'utils',
            'credentials.json'
        )

        self.gc = gspread.service_account(filename=caminho_credenciais)

        self.sh = self.gc.open_by_url(
            "https://docs.google.com/spreadsheets/d/18h61nxeQ8OgRjQCRUrDJoBceoobQLjXIgIPfpBr17Pk/edit?gid=0#gid=0"
        )

        self.worksheet = self.sh.worksheet("Links_Colaboradores")

    def buscar_funcionarios(self):
        data = self.worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])

        lista_dados = []

        for index, row in df.iterrows():
            dados = {
                "nome": row["Nome do Funcionário"],
                "link": row["Link de Compartilhamento"],
                "email": row["E-mail"],
                "empresa": row["Empresa"],
                "linha": index + 2
            }
            lista_dados.append(dados)

        return lista_dados
    
    def atualizar_link(self, linha, novo_link):
        headers = self.worksheet.row_values(1)
        print("DEBUG headers:", headers)

        headers_normalizados = [h.strip() for h in headers]

        try:
            col_index = headers_normalizados.index("Link de Compartilhamento") + 1
        except ValueError:
            raise Exception(
                f'Coluna "Link de Compartilhamento" não encontrada. Cabeçalhos encontrados: {headers_normalizados}'
            )

        print(f"DEBUG -> atualizando linha {linha}, coluna {col_index}, valor {novo_link}")

        self.worksheet.update_cell(int(linha), col_index, novo_link)

        valor_salvo = self.worksheet.cell(int(linha), col_index).value
        print(f"Valor salvo na planilha: {valor_salvo}")