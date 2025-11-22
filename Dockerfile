# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt requirements.txt

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta que o Flask vai usar
EXPOSE 5000

# Comando para rodar a aplicação
# Usamos o flask run com --host=0.0.0.0 para tornar a aplicação acessível externamente
CMD ["flask", "run"]
