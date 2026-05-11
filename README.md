# Cortador de PDF (Holerites)

## Como funciona?

Anexe os arquivos solicitados e clique em cortar, ele vai pedir para logar com a conta google,
depois ele separa os pdfs, identifica cada colaborador e coloca em cada pasta do Google Drive

## Como usar
### 1 - Clone o repositório
```
git clone https://github.com/RafaelGoncalves-bit/Cortador2.0.git
```

### 1.1 - Baixar e instalar Virtualenv
```
pip install virtualenv
python -m virtulaenv venv
```

### 1.2 - Ativar venv
#### Winodws
```
cd venv
cd Scripts
activate.bat
cd ../..
```

#### Linux
```
source venv/bin/activat
```


### 1.3 - Instale as dependências
```
pip install -r requirements.txt
```

## 1.4 - Rodar projeto
```
python manage.py runserer
```

## Ou

### 2 - Dê pull no docker

```
docker pull ghcr.io/rafaelgoncalves-bit/cortador:latest
```

# 3 - Acessar
```
localhost:8000
ou
localhost:8005
```
