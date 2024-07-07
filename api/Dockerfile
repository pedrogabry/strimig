# Use a imagem base do Python 3.9 com Ubuntu 20.04
FROM python:3.9-slim-buster

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para o diretório /app no container
COPY . /app

# Instala as dependências Python especificadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 80 para tráfego HTTP
EXPOSE 80

# Comando a ser executado quando o container for iniciado
CMD ["python3", "app.py"]
