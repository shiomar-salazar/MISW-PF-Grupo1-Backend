import traceback
from utilities.utilities import validar_token
from queries.base_query import BaseQuery
from models.models import db, Usuario
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, UserNotFound
from models.models import Usuario

# Clase que contiene la logica de consulta de usuarios
class ConsultarUsuario(BaseQuery):
    # Constructor
    def __init__(self, headers):
        self.validar_headers(headers)
        
    # Función que valida los headers del servicio
    def validar_headers(self, headers):
        # Validacion si existe el header Authorization
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                self.token = token
            else:
                raise BadRequest
        else:
            raise TokenNotFound
    
    # Función que realiza de consulta de un usuario
    def query(self):
        try:
            # Logica de negocio
            payload = validar_token(self.token)
            usuario = db.session.query(Usuario).filter_by(id = payload['id_usuario']).first()
            if usuario == None:
                raise UserNotFound
            return usuario
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
