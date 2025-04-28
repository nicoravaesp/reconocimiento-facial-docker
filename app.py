import cv2
import face_recognition
import os
import pickle
import shutil
from flask import Flask, render_template, Response, request, redirect, url_for
import numpy as np
from datetime import datetime

app = Flask(__name__)
camera = cv2.VideoCapture(0)

known_faces = []  # Lista de diccionarios: {'name': ..., 'encoding': ..., 'filename': ...}

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 📂 Funciones para guardar/cargar datos
def save_known_faces():
    with open('known_faces.pkl', 'wb') as f:
        pickle.dump(known_faces, f)

def load_known_faces():
    global known_faces
    if os.path.exists('known_faces.pkl'):
        with open('known_faces.pkl', 'rb') as f:
            known_faces = pickle.load(f)

# 📂 Descarga automática de modelos si no existen
def download_models():
    files = {
        "dlib_face_recognition_resnet_model_v1.dat": "https://drive.google.com/uc?export=download&id=1niHcxFg_AilDNGVlxn58lFsNg_H5d88J",
        "shape_predictor_68_face_landmarks.dat": "https://drive.google.com/uc?export=download&id=17yahxxX-EzjD8r3cFI6UZk6HGy5KOD77"
    }

    os.makedirs("models", exist_ok=True)

    for filename, url in files.items():
        filepath = f"models/{filename}"
        if not os.path.exists(filepath):
            os.system(f"wget {url} -O {filepath}")
            print(f"{filename} descargado correctamente.")

download_models()

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)

            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces([face['encoding'] for face in known_faces], face_encoding)
                    name = "Desconocido"

                    face_distances = face_recognition.face_distance([face['encoding'] for face in known_faces], face_encoding)
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_faces[best_match_index]['name']

                    face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 🔥 Subir imágenes o capturas
@app.route('/upload', methods=['POST'])
def upload():
    try:
        name = request.form.get('name')
        files = request.files.getlist('file')

        if not name:
            return redirect(request.url)

        person_folder = os.path.join(app.config['UPLOAD_FOLDER'], name)
        os.makedirs(person_folder, exist_ok=True)

        if not files or (len(files) == 1 and files[0].filename == ''):
            # 📸 Captura desde cámara
            file = request.files.get('file')
            if file and file.filename != '':
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'{timestamp}.png'
                filepath = os.path.join(person_folder, filename)
                file.save(filepath)

                # Procesar la imagen capturada
                image = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    known_faces.append({
                        'name': name,
                        'encoding': encodings[0],
                        'filename': f'{name}/{filename}'
                    })
                    save_known_faces()
        else:
            # 📂 Subida manual de imágenes
            for file in files:
                if file and file.filename != '':
                    filename = file.filename
                    filepath = os.path.join(person_folder, filename)
                    file.save(filepath)

                    image = face_recognition.load_image_file(filepath)
                    encodings = face_recognition.face_encodings(image)

                    for encoding in encodings:
                        known_faces.append({
                            'name': name,
                            'encoding': encoding,
                            'filename': f'{name}/{filename}'
                        })

            save_known_faces()

        return redirect(url_for('faces'))

    except Exception as e:
        print(f"Error al registrar cara: {e}")
        return f"Ocurrió un error al registrar la cara: {e}", 500

@app.route('/faces')
def faces():
    return render_template('faces.html', faces=known_faces)

@app.route('/delete_face/<name>', methods=['GET'])
def delete_face(name):
    global known_faces
    known_faces = [face for face in known_faces if face['name'] != name]
    save_known_faces()

    # 🗑️ Borrar carpeta del usuario
    person_folder = os.path.join(app.config['UPLOAD_FOLDER'], name)
    if os.path.exists(person_folder):
        shutil.rmtree(person_folder)

    return redirect(url_for('faces'))

# 🛑 Cargar caras conocidas al inicio
load_known_faces()

if __name__ == '__main__':
    app.run(debug=True)