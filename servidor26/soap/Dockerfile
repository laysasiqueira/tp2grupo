FROM python:3.10-slim
WORKDIR /app

# Instala dependências
COPY soap/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia serviço e utils
COPY soap/soap_service.py .
COPY utils/conversor_funcoes.py utils/mongodb_helper.py ./utils/

# Variáveis de ambiente
ENV AUTH_URL=http://auth:6000
ENV MESSAGING_URL=http://messaging:8000/mensagem

EXPOSE 8010
CMD ["python", "soap_service.py"]
