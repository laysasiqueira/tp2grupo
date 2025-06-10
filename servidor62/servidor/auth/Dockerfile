FROM python:3.10-slim

WORKDIR /app

COPY servidor/auth/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY servidor/auth/ .

ENV FLASK_APP=auth_service.py
ENV JWT_SECRET=${JWT_SECRET}

EXPOSE 6000
CMD ["python", "auth_service.py"]
