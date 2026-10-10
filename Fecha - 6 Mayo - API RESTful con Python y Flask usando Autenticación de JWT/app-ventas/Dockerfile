FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# app.py queda igual a la guía (host="localhost"). Para que la API sea alcanzable desde
# Windows, el contenedor la arranca con "flask run" escuchando en 0.0.0.0; --debug activa
# el reloader (hot reload) igual que debug=True.
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000", "--debug"]
