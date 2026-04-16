from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
import core.scripts.processar as processar

def index(request):
    return render(request, 'index.html')

def processar_dados(request):
    processador = processar.ProcessarDados()
    return processador.processar(request)