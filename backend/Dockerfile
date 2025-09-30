# Dockerfile para Render
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Download de dados NLTK (necessário para NLP)
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 8000

# Comando para iniciar aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]