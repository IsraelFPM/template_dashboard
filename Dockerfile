# Usa uma imagem oficial do Python, versão slim para ser mais leve
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do seu código para dentro do contêiner
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar a aplicação quando o contêiner iniciar
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]