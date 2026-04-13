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
        pdf_h = request.FILES.get('holerites')
        pdf_p = request.FILES.get('ponto')

        # Verifica se a data e os dois arquivos foram enviados
        if data_sel and pdf_h and pdf_p:
            # 1. Salva os arquivos temporariamente
            name_h = default_storage.save(f'tmp/{pdf_h.name}', pdf_h)
            name_p = default_storage.save(f'tmp/{pdf_p.name}', pdf_p)
            
            # 2. Gera o caminho absoluto (essencial para o Windows encontrar o arquivo)
            path_h = os.path.join(settings.MEDIA_ROOT, name_h)
            path_p = os.path.join(settings.MEDIA_ROOT, name_p)

            try:
                # 3. Chama o seu script
                cortar(data_sel, path_h, path_p)
                messages.success(request, "Automação executada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar script: {e}")
            
            return redirect('index')
        
        else:
            # Caso falte algum arquivo ou a data
            messages.warning(request, "Por favor, preencha a data e anexe os dois arquivos PDF.")
            return redirect('index')

    # Se alguém tentar acessar a URL via GET, volta para o index
    return redirect('index')