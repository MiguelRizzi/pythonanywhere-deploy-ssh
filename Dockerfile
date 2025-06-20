FROM python:3.11-slim

COPY deployment /deployment
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "deployment/main.py"]
