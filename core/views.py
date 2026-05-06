from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
import core.main as main
from django.http import JsonResponse, HttpResponse
from google_auth_oauthlib.flow import Flow
import os

SCOPES = ['https://www.googleapis.com/auth/drive']


def index(request):
    return render(request, 'index.html')


def processar_dados(request):
    token_path = os.path.join(settings.BASE_DIR, 'core/utils/token.json')
    if not os.path.exists(token_path):
        request.session['next'] = request.get_full_path()
        return redirect('/login-google/')
    
    processador = main.ProcessarDados()
    return processador.processar(request)


def chrome_devtools(request):
    return JsonResponse({})


# ================================
# LOGIN GOOGLE
# ================================

def login_google(request):
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'core/utils/cliente_secret.json'),
        scopes=SCOPES,
        redirect_uri='https://cortador2.agillecred.com.br/oauth2callback/'
    )

    auth_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    # SALVA TUDO QUE PRECISA
    request.session['state'] = state
    request.session['code_verifier'] = flow.code_verifier

    return redirect(auth_url)


def oauth2callback(request):
    state = request.session.get('state')
    code_verifier = request.session.get('code_verifier')

    if not state or not code_verifier:
        return HttpResponse("Sessão expirada. Tente novamente.")

    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'core/utils/cliente_secret.json'),
        scopes=SCOPES,
        state=state,
        redirect_uri='https://cortador2.agillecred.com.br/oauth2callback/'
    )

    # RESTAURA PKCE
    flow.code_verifier = code_verifier

    flow.fetch_token(
        authorization_response=request.build_absolute_uri()
    )

    creds = flow.credentials

    token_path = os.path.join(settings.BASE_DIR, 'core/utils/token.json')
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    
    next_url = request.session.get('next', '/')
    return redirect(next_url)