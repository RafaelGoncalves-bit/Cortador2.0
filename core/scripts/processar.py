from core.scripts.escritor import Escritor
from core.scripts.leitor import LeitorPdfs
from django.contrib import messages
from django.shortcuts import redirect


class ProcessarDados:

    def __init__(self):
        pass

    def processar(self, request):
        if request.method == "POST":
            escritor = Escritor()
            leitor = LeitorPdfs()

            pdfs = [
                ("holerite", request.FILES.get("holerites")),
                ("ponto", request.FILES.get("ponto")),
            ]

            pdfs = [pdf for pdf in pdfs if pdf[1] is not None]

            if not pdfs:
                messages.warning(request, "Envie pelo menos um arquivo para processar.")
                return redirect("index")

            try:
                for tipo, pdf in pdfs:
                    if not pdf:
                        continue

                    resultados = leitor.ler_pdfs(tipo, pdf)

                    for item in resultados:
                        escritor.escrever_pdfs(item["tipo"], item["nome"], item["page"])

                messages.success(request, "Arquivos processados com sucesso")

            except Exception as e:
                messages.error(request, f"Erro no processamento: {e}")

        else:
            messages.warning(request, "Método de requisição inválido.")

        return redirect("index")
