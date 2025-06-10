FROM python:3.10-slim
WORKDIR /app

COPY grpc/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY grpc/grpc_service.py .
COPY grpc/agenda_pb2.py .
COPY grpc/agenda_pb2_grpc.py .
COPY utils/mongodb_helper.py utils/conversor_funcoes.py ./utils/

ENV AUTH_URL=http://auth:6000
ENV MESSAGING_URL=http://messaging:8000/mensagem

EXPOSE 50051
CMD ["python", "grpc_service.py"]
