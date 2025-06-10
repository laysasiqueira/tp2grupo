FROM python:3.10-slim

WORKDIR /app

# Copia requirements (só flask e pika)
COPY servidor/messaging/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o proxy e o helper
COPY servidor/messaging/messaging_service_app.py .
COPY servidor/messaging/rabbitmq_helper.py .

EXPOSE 8000

CMD ["python", "messaging_service_app.py"]
