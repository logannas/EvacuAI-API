# Etapa base com Python
FROM python:3.11-slim

# Variável de ambiente para não gerar .pyc e usar UTF-8
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/Sao_Paulo

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala dependências do Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Expõe a porta padrão do Uvicorn
EXPOSE 8000

# Comando para rodar a API com reload (modo desenvolvimento)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
