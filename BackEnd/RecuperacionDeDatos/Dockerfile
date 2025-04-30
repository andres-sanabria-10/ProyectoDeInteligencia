# Dockerfile
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que corre tu app Flask
EXPOSE 5000

# Comando para ejecutar la app Flask
CMD ["python", "app.py"]
