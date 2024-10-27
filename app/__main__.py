from flask import Flask
from flask_cors import CORS
from app.database.conector import DatabaseConector, db
from app.routes.votante_routes import votante_bp
from app.utils.img_convert_utils import convert_images_to_files
from app.utils.face_recognition_utils import (
    load_reference_encodings,
    train_recognizer
)

app = Flask(__name__)

CORS(app)

db_config = DatabaseConector(app)

def create_db_and_tables():
    db.create_all()
    convert_images_to_files()  

app.register_blueprint(votante_bp)

with app.app_context():
    create_db_and_tables()  
    reference_encodings, labels, label_dict = load_reference_encodings()
    recognizer = train_recognizer(reference_encodings, labels)

    app.config["FACE_RECOGNIZER"] = recognizer
    app.config["LABEL_DICT"] = label_dict


if __name__ == "__main__":
    app.run(debug=True)
