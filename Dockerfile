FROM python:3.11-slim

# Coincide con el --workdir que usa GitHub Actions
WORKDIR /github/workspace

# Copiamos todo el contenido del repo en esa ruta
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "deployment/main.py"]
