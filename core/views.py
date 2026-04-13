import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .scripts.cortador import cortar
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def processar_dados(request):
    if request.method == 'POST':
        data_sel = request.POST.get('data')
        
        # Aqui pegamos o arquivo bruto que está na memória RAM
        pdf_h = request.FILES.get('holerites')
        pdf_p = request.FILES.get('ponto')

        if data_sel and pdf_h and pdf_p:
            try:
                # Passamos os objetos de arquivo diretamente para o script
                cortar(data_sel, pdf_h, pdf_p)
                messages.success(request, "Processamento concluído com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro no processamento: {e}")
        else:
            messages.warning(request, "Preencha todos os campos e anexe os arquivos.")
            
        return redirect('index')
    return redirect('index')