FROM python:3.11-slim

WORKDIR /app

COPY deployment /app/deployment
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY deployment/main.py /app/deployment/main.py

ENTRYPOINT ["python", "deployment/main.py"]