# Imagen base ligera de Python.
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor.
WORKDIR /app

# Primero copiamos e instalamos las dependencias para aprovechar la caché de
# capas de Docker (si el código cambia pero las dependencias no, no se reinstalan).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación.
COPY . .

# Puerto en el que escucha la aplicación.
EXPOSE 5000

# Arranque con gunicorn (servidor WSGI de producción).
# "app:app" significa: en el archivo app.py, usar el objeto Flask llamado 'app'.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
