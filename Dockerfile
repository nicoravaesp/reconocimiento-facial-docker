FROM python:3.10-slim

# Instalamos las dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Definimos el directorio de trabajo
WORKDIR /app

# Copiamos primero el requirements.txt
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Comando para ejecutar la app
CMD ["python", "app.py"]
