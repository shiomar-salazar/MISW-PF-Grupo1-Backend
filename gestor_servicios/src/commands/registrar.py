# Importación de dependencias
import os
from commands.base_command import BaseCommannd
from utilities.utilities import consumir_servicio_usuarios
from validators.validators import validar_esquema, esquema_registro_servicio, validar_headers, validar_permisos_usuario
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, ServiceAlreadyRegistered
from models.models import db, Servicios
import traceback

# Clase que contiene la logica del registro de un servicio
class RegistrarServicio(BaseCommannd):
    # Constructor
    def __init__(self, data, headers):
        validar_headers(headers)
        self.headers = headers
        self.validar_request(data)
        self.asignar_datos_servicio(data)

    # Función que valida el request del servicio
    def validar_request(self, json_payload):
        # Validacion del request
        validar_esquema(json_payload, esquema_registro_servicio)
        
    # Función que valida el request del servicio
    def asignar_datos_servicio(self, json_payload):
        # Asignacion de variables
        self.nombre = json_payload['nombre']
        self.descripcion = json_payload['descripcion']
        self.frecuencia = json_payload['frecuencia']
        self.costo = json_payload['costo']
        self.numero_minimo_participantes = json_payload['numero_minimo_participantes']
        self.numero_maximo_participantes = json_payload['numero_maximo_participantes']
        self.lugar = json_payload['lugar']
        self.fecha = json_payload['fecha']
        self.horario = json_payload['horario']
        self.id_usuario = json_payload['id_usuario']

        
    # Función que realiza el registro del usuario en BD
    def registrar_servicio_bd(self):
        # Registrar en BD
        servicio = Servicios(
            nombre=self.nombre, 
            descripcion=self.descripcion,  
            frecuencia=self.frecuencia,  
            costo=self.costo, 
            numero_minimo_participantes=self.numero_minimo_participantes,  
            numero_maximo_participantes=self.numero_maximo_participantes, 
            lugar=self.lugar, 
            fecha=self.fecha, 
            horario=self.horario, 
            id_usuario=self.id_usuario
        )
        db.session.add(servicio)
        db.session.commit()
        return servicio

    # Función que realiza creación del servicio
    def execute(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            servicio_registrado = self.registrar_servicio_bd()
            return servicio_registrado.to_dict()
        except IntegrityError as e:# pragma: no cover
            traceback.print_exc()
            db.session.rollback()
            raise ServiceAlreadyRegistered(e)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        