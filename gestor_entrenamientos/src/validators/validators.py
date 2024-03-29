# Importación de dependencias
from errors.errors import BadRequest
from jsonschema import validate
import traceback
import jsonschema

# Esquemas
# Esquema para las alertas
alertaSchema = {
    "type": "object",
    "properties": {
        "id_trigger": {"type": "string", "minimum": 4, "maximum": 64},
        "latitud": {"type": "string", "minimum": 6, "maximum": 64},
        "longitud": {"type": "string", "minimum": 6, "maximum": 64},
        "descripcion":  {"type": "string", "minimum": 3, "maximum": 64},
    },
    "required": ["id_trigger", "latitud", "longitud", "descripcion"]
}

planEntrenamientoEsquema = {
    "type": "object",
    "properties": {
        "sexo": {"type": "string", "enum" : ["MASCULINO", "FEMENINO"]},
        "peso": {"type": "integer", "minimum": 40, "maximum": 200},  #kilogramos
        "estatura": {"type": "integer", "minimum": 140, "maximum": 200},  #centimetros
        "edad": {"type": "integer", "minimum": 18, "maximum": 90},
        "enfermedades_cardiovasculares": {"type": "string", "enum" : ["SI", "NO"]},
        "practica_deporte": {"type": "string", "enum" : ["SI", "NO"]},
        "proposito": {"type": "string", "enum" : ["GANAR MASA MUSCULAR", "PERDER PESO"]}
    },
    "required": ["sexo", "peso", "estatura", "edad", "enfermedades_cardiovasculares", "practica_deporte", "proposito"]
}

# Función que valida los esquemas de las peticiones
def validateSchema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest