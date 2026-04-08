from django.shortcuts import render

def cortador(request):
    return render(request, 'index.html')
