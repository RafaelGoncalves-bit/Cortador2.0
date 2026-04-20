from core.scripts.escritor import Escritor
from core.scripts.leitor import LeitorPdfs
from django.contrib import messages
from django.shortcuts import redirect
from core.scripts.drive import GoogleDrive
from core.scripts.sheets import BuscarFuncionarios
from core.scripts.comparar_nomes import Comparador


class ProcessarDados:

    def __init__(self):
        self.drive = GoogleDrive()
        self.leitor = LeitorPdfs()

        buscar = BuscarFuncionarios()
        self.funcionarios = buscar.buscar_funcionarios()

        self.comparador = Comparador(self.funcionarios)

        # passa o drive pro escritor
        self.escritor = Escritor(self.drive)

    def processar(self, request):

        if request.method != "POST":
            messages.warning(request, "Método de requisição inválido.")
            return redirect("index")

        pdfs = [
            ("holerite", request.FILES.get("holerites")),
            ("ponto", request.FILES.get("ponto")),
        ]
        
        data = request.POST.get("data")

        pdfs = [pdf for pdf in pdfs if pdf[1] is not None]

        if not pdfs:
            messages.warning(request, "Envie pelo menos um arquivo para processar.")
            return redirect("index")

        try:
            for tipo, pdf in pdfs:

                resultados = self.leitor.ler_pdfs(tipo, pdf)

                # comparação 
                dados_comparados = self.comparador.comparar(resultados)

                for item in dados_comparados:

                    if item["status"] == "não encontrado":
                        print(f"{item['nome']} não encontrado - pulando")
                        continue
                    
                    id_pasta_destino = self.drive.criar_pasta(
                        nome_pasta=data, 
                        parent_id=item["pasta_id"]
                    )
                    # ENVIA PRO DRIVE
                    self.escritor.escrever_pdfs(
                        tipo,
                        item["nome"],
                        item["page"],
                        id_pasta_destino
                    )

            messages.success(request, "Arquivos processados com sucesso")

        except Exception as e:
            messages.error(request, f"Erro no processamento: {e}")

        return redirect("index")