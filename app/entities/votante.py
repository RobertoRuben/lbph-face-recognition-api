from app.database.conector import db

class Votante(db.Model):
    __tablename__ = "usuario_votante"

    id_usuario = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Numeric(precision=8, scale=0), nullable=False, unique=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido_paterno = db.Column(db.String(255), nullable=False)
    apellido_materno = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    foto = db.Column(db.Text, nullable=True)

    def __init__(self, dni, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, email, password, foto):
        self.dni = dni
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.fecha_nacimiento = fecha_nacimiento
        self.email = email
        self.password = password
        self.foto = foto
