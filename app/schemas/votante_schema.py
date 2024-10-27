from marshmallow import Schema, fields, validates, ValidationError, validate

class VotanteSchema(Schema):
    id_usuario = fields.Int(dump_only=True)
    
    dni = fields.Int(
        required=True,
        error_messages={"required": "El DNI es obligatorio"}
    )
    
    nombre = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "El nombre es obligatorio"}
    )
    
    apellido_paterno = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "El apellido paterno es obligatorio"}
    )
    
    apellido_materno = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "El apellido materno es obligatorio"}
    )
    
    fecha_nacimiento = fields.Date(
        required=True,
        error_messages={"required": "La fecha de nacimiento es obligatoria"}
    )
    
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El correo electrónico es obligatorio",
            "invalid": "El correo electrónico no es válido"
        }
    )
    
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        error_messages={
            "required": "La contraseña es obligatoria",
            "invalid": "La contraseña debe tener al menos 8 caracteres"
        }
    )
    
    foto = fields.Raw(allow_none=True)

    @validates("dni")
    def validate_dni(self, value):
        if not (10000000 <= value <= 99999999):
            raise ValidationError("El DNI debe tener exactamente 8 dígitos numéricos")

    @validates("nombre")
    def validate_nombre(self, value):
        if not value.strip():
            raise ValidationError("El nombre no puede estar en blanco")

    @validates("apellido_paterno")
    def validate_apellido_paterno(self, value):
        if not value.strip():
            raise ValidationError("El apellido paterno no puede estar en blanco")

    @validates("apellido_materno")
    def validate_apellido_materno(self, value):
        if not value.strip():
            raise ValidationError("El apellido materno no puede estar en blanco")
