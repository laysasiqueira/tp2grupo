FROM python:3.10-slim

WORKDIR /app

COPY servidor/rest/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY servidor /app/servidor

ENV FLASK_APP=rest/api.py
ENV MONGO_URL=${MONGO_URL}
ENV RABBITMQ_HOST=${RABBITMQ_HOST}
ENV AUTH_URL=${AUTH_URL}

EXPOSE 5050
CMD ["python", "/app/servidor/rest/api.py"]

