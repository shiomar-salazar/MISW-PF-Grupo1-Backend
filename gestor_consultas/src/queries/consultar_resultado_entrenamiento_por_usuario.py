import traceback
from validators.validators import validar_permisos_usuario
from utilities.utilities import consumir_servicio_usuarios
from queries.base_query import BaseQuery
from models.models import db, ResultadosEntrenamiento, ConsultaResultadosEntrenamientoSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, NoRecordsFound


consulta_resultado_entrenamiento_schema = ConsultaResultadosEntrenamientoSchema()

# Clase que contiene la logica de consulta resultados de entrenamiento con base al id_usuario
class ConsultarResultadoEntrenamientoPorUsuario(BaseQuery):
    # Constructor
    def __init__(self, id_usuario, headers):
        self.validate_request(id_usuario)
        self.validar_headers(headers)
        
    # Función que valida los headers del servicio
    def validar_headers(self, headers):
        # Validacion si existe el header Authorization
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            # Verificar si el encabezado Authorization comienza con "Bearer"
            if not auth_header.startswith('Bearer '):
                raise BadRequest
            self.headers = headers
        else:
            raise TokenNotFound

    # Función que valida el request del servicio
    def validate_request(self, id_usuario):
        if id_usuario == None:
            raise BadRequest
        self.id_usuario = id_usuario
    
    # Función que realiza la consulta resultados de entrenamiento con base al id_usuario
    def query(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            resultado_entrenamiento_usuario = db.session.query(ResultadosEntrenamiento).filter(ResultadosEntrenamiento.id_usuario == self.id_usuario).all()
            if resultado_entrenamiento_usuario == None:
                raise NoRecordsFound
            return [consulta_resultado_entrenamiento_schema.dump(resultado) for resultado in resultado_entrenamiento_usuario]
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            db.session.rollback()
            raise ApiError(e)
        
