FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copiar código da aplicação
COPY src/ ./src/
COPY tests/ ./tests/
COPY pyproject.toml ./
COPY env.example .env

# Expor porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

