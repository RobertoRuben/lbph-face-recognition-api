from app.database.conector import db
from app.entities.votante import Votante
from sqlalchemy.exc import SQLAlchemyError

class VotanteRepository:

    @staticmethod
    def create(dni, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, email, password, foto=None):
        new_votante = Votante(
            dni=dni,
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            fecha_nacimiento=fecha_nacimiento,
            email=email,
            password=password,
            foto=foto
        )
        try:
            db.session.add(new_votante)
            db.session.commit()
            return new_votante
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_id(votante_id):
        return Votante.query.get(votante_id)

    @staticmethod
    def get_all():
        return Votante.query.all()

    @staticmethod
    def update(votante_id, dni=None, nombre=None, apellido_paterno=None, apellido_materno=None, fecha_nacimiento=None, email=None, password=None, foto=None):
        votante = Votante.query.get(votante_id)
        if not votante:
            return None
        
        if dni:
            votante.dni = dni
        if nombre:
            votante.nombre = nombre
        if apellido_paterno:
            votante.apellido_paterno = apellido_paterno
        if apellido_materno:
            votante.apellido_materno = apellido_materno
        if fecha_nacimiento:
            votante.fecha_nacimiento = fecha_nacimiento
        if email:
            votante.email = email
        if password:
            votante.password = password
        if foto is not None:  # Permite asignar `None` explícitamente a `foto`
            votante.foto = foto

        try:
            db.session.commit()
            return votante
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(votante_id):
        votante = Votante.query.get(votante_id)
        if not votante:
            return False

        try:
            db.session.delete(votante)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def exists_by_dni(dni):
        return Votante.query.filter_by(dni=dni).first() is not None
    

    @staticmethod
    def get_by_dni(dni):
        return Votante.query.filter_by(dni=dni).first()
