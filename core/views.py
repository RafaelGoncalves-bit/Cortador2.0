import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .scripts.cortador import Cortador
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def processar_dados(request):
    if request.method == 'POST':
        pdf_h = request.FILES.get('holerites')
        pdf_p = request.FILES.get('ponto')
        cortador = Cortador()
        
        if pdf_h and pdf_p:
            try:
                cortador.cortar_holerite(pdf_h)
                cortador.cortar_ponto(pdf_p)
                messages.success(request, "Holerites e Ponos processados com sucesso")
            except Exception as e:
                messages.error(request, f"Erro no processamento: {e}")
        elif pdf_h:
            try:
                cortador.cortar_holerite(pdf_h)
                messages.success(request, "Holerites Processados com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro no processamento: {e}")
        elif pdf_p:
            try:
                cortador.cortar_ponto(pdf_p)
                messages.success(request, "Ponto Processados com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro no processamento: {e}")
        else:
            messages.warning(request, "Preencha todos os campos e anexe os arquivos.")
            
        return redirect('index')
    return redirect('index')