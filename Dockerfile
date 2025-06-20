FROM python:3.11-slim

WORKDIR /app

COPY deployment /app/deployment
COPY requirements.txt /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "deployment/main.py"]
