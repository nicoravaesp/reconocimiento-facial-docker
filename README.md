# Reconocimiento Facial con Python 3.10(tiene que ser esa version) y Flask

Este proyecto implementa un sistema de reconocimiento facial utilizando Python y Flask. Permite identificar rostros en imágenes y en tiempo real desde una cámara web.

## pasos para correr en docker:(tener en cuentas las caracteristicas del proyecto)

# Reconocimiento Facial - Dockerizado  

Este repositorio contiene una aplicación de reconocimiento facial, configurada para ejecutarse dentro de un contenedor Docker.  

### 1. Clonar el repositorio  

### 2. Construir la imagen Docker

Ejecuta el siguiente comando para construir la imagen del proyecto:

docker build -t reconocimiento-facial .

### 3. ejecuta el siguiente comando

docker run --rm --device=/dev/video0 -p 5000:5000 mi-proyecto 
## esto hace que se le den permisos a las camaras en el contenedor por eso ahi que ejecutarlo asi.

## Características

- Identificación de rostros conocidos a partir de imágenes entrenadas.
- Interfaz web simple para subir y procesar imágenes.
- Integración con cámara en vivo para detección en tiempo real.

## Requisitos
✅ 1. Verificar que tenés Python 3.10 instalado

Ejecutá:

python3.10 --version

Si ves algo como Python 3.10.x, podés avanzar.
Si NO está instalado, instalalo con:

sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

✅ 2. Crear un nuevo entorno virtual con Python 3.10

Dentro de tu carpeta del proyecto (~/reconocimiento-facial):

python3.10 -m venv venv310

Esto crea un nuevo entorno llamado venv310.
✅ 3. Activar el nuevo entorno

source venv310/bin/activate

Vas a ver algo como:

(venv310) nicolas@kali:~/reconocimiento-facial$

✅ 4. Instalar las dependencias correctamente

Con el nuevo entorno activo:

pip install --upgrade pip
pip install -r requirements.txt

Si te da errores con face_recognition, usá:

pip install cmake
pip install dlib
pip install face_recognition
pip install git+https://github.com/ageitgey/face_recognition_models

✅ 5. Correr tu app con Python 3.10

Asegurate de estar en el entorno venv310, y luego:

python app.py


Antes de ejecutar el proyecto, asegúrate de tener las siguientes dependencias instaladas:

```bash
pip install -r requirements.txt

Clona el repositorio:
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>

Ejecuta la aplicación:
python app.py

Abre tu navegador y accede a http://127.0.0.1:5000/.

/dataset/          # Imágenes de entrenamiento
/images/           # Archivos de imágenes subidas por el usuario
/models/           # Modelos entrenados (.pkl, .h5)
/static/           # Archivos estáticos (CSS, JS)
/templates/        # Archivos HTML
app.py             # Código principal de la aplicación
requirements.txt   # Dependencias necesarias
.gitignore         # Archivos ignorados en Git

Contribuir
Si deseas mejorar el proyecto, por favor haz un fork del repositorio, trabaja en tus cambios y envía un pull request.

Licencia
Este proyecto está bajo la licencia MIT.

Puedes modificar el contenido para agregar información específica sobre tu implementación. ¿Te gustaría incluir detalles sobre el modelo de reconocimiento facial que estás usando o mejorar alguna sección?
```
