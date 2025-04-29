FROM python:3.10-slim

# Instalamos dependencias necesarias para compilar dlib y opencv correctamente
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-dev \
    liblapack-dev \
    libopenblas-dev \
    libboost-python-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
