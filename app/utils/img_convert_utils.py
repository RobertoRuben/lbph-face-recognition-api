import base64
import os
from app.database.conector import db
from app.entities.votante import Votante

IMAGE_DIRECTORY = "app/img"

def convert_images_to_files():
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)
    
    votantes = Votante.query.all()

    for votante in votantes:
        if votante.foto:  
            image_data = base64.b64decode(votante.foto)
            
            filename = f"{votante.dni}.jpg"
            filepath = os.path.join(IMAGE_DIRECTORY, filename)
            
            with open(filepath, "wb") as image_file:
                image_file.write(image_data)
            print(f"Imagen guardada como {filepath}")
