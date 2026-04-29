
import os
from dotenv import load_dotenv
from core.service.pdf.escritor_service import Escritor
from core.service.pdf.leitor_service import LeitorPdfs
from django.contrib import messages
from django.shortcuts import redirect
from core.service.drive.drive_service import Drive
from core.service.sheets_service import BuscarFuncionarios
from core.service.comparar_nomes_service import Comparador


class ProcessarDados:

    def __init__(self):
        load_dotenv() #Carrega arquivo .ENV
        
        #Pega os valores do .ENV
        self.PASTA_RAIZ = os.getenv('PASTA_RAIZ')
        
        #Define as classes
        self.drive = Drive()
        self.leitor = LeitorPdfs()
        self.sheets = BuscarFuncionarios()
        self.funcionarios = self.sheets.buscar_funcionarios()
        self.comparador = Comparador(self.funcionarios)
        self.escritor = Escritor(self.drive)

    def processar(self, request):

        if request.method != "POST":
            messages.warning(request, "Método de requisição inválido.")
            return redirect("index")

        pdfs = [
            ("holerite", request.FILES.get("holerites")),
            ("ponto", request.FILES.get("ponto")),
        ]
        
        data = request.POST.get("data")  # ex: 04-2026

        pdfs = [pdf for pdf in pdfs if pdf[1] is not None]

        if not pdfs:
            messages.warning(request, "Envie pelo menos um arquivo para processar.")
            return redirect("index")

        try:
            for tipo, pdf in pdfs:

                resultados = self.leitor.ler_pdfs(tipo, pdf)

                dados_comparados = self.comparador.comparar(resultados)

                for item in dados_comparados:

                    if item["status"] == "não encontrado":
                        print(f"{item['nome']} não encontrado - pulando")
                        continue

                    nome = item["nome"]
                    link = item.get("link")
                    linha = item.get("linha")  # ESSENCIAL

                    # tenta extrair ID
                    pasta_funcionario_id = self.drive.extrair_id_pasta(link)

                    if not pasta_funcionario_id:
                        pasta_funcionario_id = self.drive.criar_ou_buscar_pasta(
                        nome,
                        self.PASTA_RAIZ
                        )

                        link_novo = f"https://drive.google.com/drive/folders/{pasta_funcionario_id}"

                        if linha is not None:
                            self.sheets.atualizar_link(linha, link_novo)
                            print(f"✅ Planilha atualizada para {nome}")
                        else:
                            print(f"❌ Linha não encontrada para {nome}")

                        link_novo = f"https://drive.google.com/drive/folders/{pasta_funcionario_id}"

                        # ATUALIZA PLANILHA
                        if linha:
                            self.sheets.atualizar_link(linha, link_novo)
                            print(f"Planilha atualizada para {nome}")

                    # cria pasta do mês
                    pasta_mes_id = self.drive.criar_ou_buscar_pasta(
                        data,
                        pasta_funcionario_id
                    )

                    # ENVIA PRO DRIVE
                    self.escritor.escrever_pdfs(
                        tipo,
                        nome,
                        item["page"],
                        pasta_mes_id
                    )

            messages.success(request, "Arquivos processados com sucesso")

        except Exception as e:
            messages.error(request, f"Erro no processamento: {e}")

        return redirect("index")