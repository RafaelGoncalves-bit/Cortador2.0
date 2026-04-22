FROM python:3.11-slim

# Melhor práticas Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências do sistema (mínimo necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro (melhora cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia projeto
COPY . .

# Porta padrão
EXPOSE 8000

# Comando produção
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cortador2.wsgi:application"]