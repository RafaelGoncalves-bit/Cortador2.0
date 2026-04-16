from core.scripts.cortador import Cortador
from django.contrib import messages
from django.shortcuts import redirect


class ProcessarDados:

    def __init__(self):
        # A classe não necessita de inicialização no momento.
        pass

    def processar(self, request):
        if request.method == "POST":
            pdf_h = request.FILES.get("holerites")
            pdf_p = request.FILES.get("ponto")
            cortador = Cortador()

            try:
                if pdf_h:
                    cortador.cortar_holerite(pdf_h)
                if pdf_p:
                    cortador.cortar_ponto(pdf_p)
                if pdf_p or pdf_h:
                    messages.success(request, "Holerites e Ponos processados com sucesso")
                else:
                    messages.warning(request, "Preencha todos os campos e anexe o/os arquivo(s).")
            except Exception as e:
                    messages.error(request, f"Erro no processamento: {e}")
                
        

        return redirect("index")
