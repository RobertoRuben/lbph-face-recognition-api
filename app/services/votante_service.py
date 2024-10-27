from flask import current_app
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash
from app.repository.votante_repository import VotanteRepository
from app.schemas.votante_schema import VotanteSchema
from marshmallow import ValidationError
from app.utils.img_convert_utils import convert_images_to_files
from app.utils.face_recognition_utils import (
    load_reference_encodings,
    train_recognizer
)

class VotanteService:

    @staticmethod
    def create_votante(data, foto=None):
        schema = VotanteSchema()
        try:
            votante_data = schema.load(data)
            
            if VotanteRepository.exists_by_dni(votante_data["dni"]):
                return {"error": "Ya existe un votante con el mismo DNI"}, 400
            
            password_hash = generate_password_hash(votante_data["password"])

            votante = VotanteRepository.create(
                dni=votante_data["dni"],
                nombre=votante_data["nombre"],
                apellido_paterno=votante_data["apellido_paterno"],
                apellido_materno=votante_data["apellido_materno"],
                fecha_nacimiento=votante_data["fecha_nacimiento"],
                email=votante_data["email"],
                password=password_hash, 
                foto=foto
            )

            votante_data = schema.dump(votante)
            votante_data.pop("password", None)
            votante_data.pop("foto", None)

            return votante_data, 201
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500


    @staticmethod
    def get_votante_by_id(votante_id):
        votante = VotanteRepository.get_by_id(votante_id)
        if not votante:
            return {"error": "Votante no encontrado"}, 404
        return VotanteSchema().dump(votante), 200


    @staticmethod
    def get_votante_by_dni(dni):
        votante = VotanteRepository.get_by_dni(dni)
        if not votante:
            return {"error": "Votante no encontrado"}, 404
        return VotanteSchema().dump(votante), 200


    @staticmethod
    def get_all_votantes():
        votantes = VotanteRepository.get_all()
        return VotanteSchema(many=True).dump(votantes), 200


    @staticmethod
    def update_votante(votante_id, data):
        schema = VotanteSchema(partial=True)
        try:
            existing_votante = VotanteRepository.get_by_id(votante_id)
            if not existing_votante:
                return {"error": "Votante no encontrado"}, 404

            votante_data = schema.load(data)
            
            if "dni" in votante_data and existing_votante.dni != votante_data["dni"]:
                if VotanteRepository.exists_by_dni(votante_data["dni"]):
                    return {"error": "Ya existe otro votante con el mismo DNI"}, 400

            password_hash = (
                generate_password_hash(votante_data["password"]) if "password" in votante_data else existing_votante.password
            )

            votante = VotanteRepository.update(
                votante_id=votante_id,
                dni=votante_data.get("dni"),
                nombre=votante_data.get("nombre"),
                apellido_paterno=votante_data.get("apellido_paterno"),
                apellido_materno=votante_data.get("apellido_materno"),
                fecha_nacimiento=votante_data.get("fecha_nacimiento"),
                email=votante_data.get("email"),
                password=password_hash,
                foto=votante_data.get("foto")
            )

            votante_data = schema.dump(votante)
            votante_data.pop("password", None)

            return votante_data, 200
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500


    @staticmethod
    def delete_votante(votante_id):
        deleted = VotanteRepository.delete(votante_id)
        if not deleted:
            return {"error": "Votante no encontrado o no pudo ser eliminado"}, 404
        return {"message": "Votante eliminado exitosamente"}, 200
