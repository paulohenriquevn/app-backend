# Usando uma imagem base leve do Python
FROM python:3.11

# Definir o diretório de trabalho como a pasta "app"
WORKDIR /app

# Copiar primeiro os arquivos essenciais (melhora cache do Docker)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
COPY requirements.txt /app/

# Define a variável de ambiente para evitar que o Flask rode em modo interativo
ENV FLASK_APP=app.py

# Expor a porta usada pela aplicação
EXPOSE 8000
EXPOSE 8765


# Comando para rodar a aplicação no local correto
CMD ["python", "/app/app.py"]
