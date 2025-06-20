FROM python:3.11-slim


COPY deployment /deployment
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN ls


CMD ["python", "deployment/main.py"]
