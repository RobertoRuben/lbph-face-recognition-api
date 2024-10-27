import cv2
import numpy as np
import os
import base64

def load_reference_encodings(img_directory="app/img"):
    reference_encodings = []
    labels = []
    label_dict = {}
    label_id = 0

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for filename in os.listdir(img_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(img_directory, filename)

            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print(f"Error: No se pudo cargar la imagen {filename}")
                continue

            faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
            if len(faces) == 0:
                print(f"No se encontraron rostros en la imagen {filename}")
                continue

            for (x, y, w, h) in faces:
                face_roi = image[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (200, 200))  

                reference_encodings.append(face_roi)
                labels.append(label_id)


            name = os.path.splitext(filename)[0]
            label_dict[label_id] = name
            label_id += 1

    return reference_encodings, labels, label_dict

def train_recognizer(reference_encodings, labels):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(reference_encodings, np.array(labels))
    return recognizer


def recognize_person(base64_image, recognizer, label_dict):
    if "," in base64_image:
        base64_image = base64_image.split(",")[1]

    try:
        image_data = base64.b64decode(base64_image)
        np_image = np.frombuffer(image_data, dtype=np.uint8)
        frame = cv2.imdecode(np_image, cv2.IMREAD_GRAYSCALE)
    except Exception as e:
        print(f"Error al decodificar la imagen base64: {e}")
        return "Desconocido"

    if frame is None:
        print("Error: No se pudo decodificar la imagen base64.")
        return "Desconocido"

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return "Desconocido"

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200, 200))

        label, confidence = recognizer.predict(face_roi)
        print(f"Etiqueta: {label}, Confianza: {confidence}")

        if confidence < 100:
            person_name = label_dict[label]
            return person_name
        else:
            return "Desconocido"