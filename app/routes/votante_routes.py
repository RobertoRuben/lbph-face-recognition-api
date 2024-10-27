import base64
from werkzeug.security import generate_password_hash
from flask import Blueprint, request, jsonify, current_app
from app.services.votante_service import VotanteService
from app.utils.face_recognition_utils import recognize_person

votante_bp = Blueprint('votante_bp', __name__)

@votante_bp.route('/votantes', methods=['POST'])
def create_votante():
    data = request.form.to_dict() 
    foto = request.files.get('foto')  

    foto_base64 = base64.b64encode(foto.read()).decode('utf-8') if foto else None

    result, status_code = VotanteService.create_votante(data, foto=foto_base64)
    return jsonify(result), status_code


@votante_bp.route('/votantes', methods=['GET'])
def get_all_votantes():
    result, status_code = VotanteService.get_all_votantes()
    return jsonify(result), status_code


@votante_bp.route('/votantes/<int:votante_id>', methods=['PUT'])
def update_votante(votante_id):
    data = request.get_json()
    result, status_code = VotanteService.update_votante(votante_id, data)
    return jsonify(result), status_code


@votante_bp.route('/votantes/<int:votante_id>', methods=['DELETE'])
def delete_votante(votante_id):
    result, status_code = VotanteService.delete_votante(votante_id)
    return jsonify(result), status_code


@votante_bp.route('/reconocimiento', methods=['POST'])
def reconocimiento_facial():
    data = request.get_json()
    base64_image = data.get("image")  

    if not base64_image:
        return jsonify({"error": "La imagen en formato base64 es requerida"}), 400

    recognizer = current_app.config['FACE_RECOGNIZER']
    label_dict = current_app.config['LABEL_DICT']

    nombre_coincidencia = recognize_person(base64_image, recognizer, label_dict)

    try:
        dni = int(nombre_coincidencia)
    except ValueError:
        return jsonify({"error": "El DNI reconocido no es válido"}), 400

    result, status_code = VotanteService.get_votante_by_dni(dni)
    
    if status_code != 200:
        return jsonify(result), status_code
    
    votante_data = {
        "apellido_materno": result.get("apellido_materno"),
        "apellido_paterno": result.get("apellido_paterno"),
        "dni": result.get("dni"),
        "email": result.get("email"),
        "fecha_nacimiento": result.get("fecha_nacimiento"),
        "id_usuario": result.get("id_usuario"),
        "nombre": result.get("nombre")
    }

    return jsonify(votante_data), 200