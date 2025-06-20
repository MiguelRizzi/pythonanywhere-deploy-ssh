FROM python:3.11-slim

WORKDIR /github/workspace

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "deployment/main.py"]
