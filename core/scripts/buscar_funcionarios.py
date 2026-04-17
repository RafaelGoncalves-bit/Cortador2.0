import gspread
import pandas as pd

class BuscarFuncionarios:
    def __init__(self):
        self.gc = gspread.service_account(filename='../utils/credentials.json')
        self.sh = self.gc.open_by_url("https://docs.google.com/spreadsheets/d/18h61nxeQ8OgRjQCRUrDJoBceoobQLjXIgIPfpBr17Pk/edit?gid=0#gid=0")
        self.worksheet = self.sh.worksheet("Links_Colaboradores")

    def buscar_funcionarios(self):
        data = self.worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        listadados = []
        
        #Mapeia as colunas
        for _, row in df.iterrows():
            nome = row["Nome do Funcionário"]
            link = row["Link de Compartilhamento"]
            email = row["E-mail"]
            empresa = row["Empresa"]
            dados = {"nome": nome, "link": link, "email": email, "empresa": empresa}
            listadados.append(dados)

            print(listadados)
            
    
# buscar = BuscarFuncionarios()
# df = buscar.buscar_funcionarios()
