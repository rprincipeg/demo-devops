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

# Nota: NO se fija un EXPOSE con puerto estático. Render asigna el puerto de
# forma dinámica a través de la variable de entorno PORT; declarar EXPOSE 5000
# solo generaba confusión y no refleja el puerto real en producción.

# Arranque con gunicorn (servidor WSGI de producción).
# "app:app" significa: en el archivo app.py, usar el objeto Flask llamado 'app'.
# Usamos la forma "shell" del CMD para que $PORT se expanda: Render inyecta la
# variable de entorno PORT y gunicorn debe escuchar exactamente en ese puerto.
# La forma "exec" (con corchetes) NO expande variables de entorno.
CMD gunicorn --bind 0.0.0.0:$PORT app:app
