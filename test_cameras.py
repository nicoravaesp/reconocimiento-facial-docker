import cv2

print("Buscando cámaras disponibles...")

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✅ Cámara encontrada en el índice {i}")
        cap.release()
    else:
        print(f"❌ No hay cámara en el índice {i}")
