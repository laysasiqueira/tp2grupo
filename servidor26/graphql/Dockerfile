FROM python:3.10-slim
WORKDIR /app

COPY graphql/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY graphql/graphql_service.py .
COPY utils/mongodb_helper.py utils/conversor_funcoes.py ./utils/

ENV AUTH_URL=http://auth:6000
ENV MESSAGING_URL=http://messaging:8000/mensagem

EXPOSE 5000
CMD ["python", "graphql_service.py"]
