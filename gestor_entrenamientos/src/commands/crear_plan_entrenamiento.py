# Importación de dependencias
import traceback
from commands.base_command import BaseCommannd
from validators.validators import validar_headers, validar_permisos_usuario, validar_esquema, crear_plan_entrenamiento_esquema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, BadRequest, TokenNotFound
from models.models import db, Entrenamientos, PlanEntrenamiento, EntrenamientoSchema
from utilities.utilities import consumir_servicio_usuarios

# Esquemas
entrenamiento_schema = EntrenamientoSchema()

# Clase que contiene la logica de creción de un plan de entrenamiento       
class CrearPlanEntrenamiento(BaseCommannd):
    def __init__(self, data, headers):
        validar_headers(headers)
        self.headers = headers    
        self.validar_request(data)
        self.asignar_datos(data)

    # Función que valida el request del servicio
    def validar_request(self, request_json):
        # Validacion del request
        validar_esquema(request_json, crear_plan_entrenamiento_esquema)

    # Función que valida el request del servicio
    def asignar_datos(self, json_payload):
        # Asignacion de variables
        self.entrenamiento = json_payload['entrenamiento']
        self.numero_semanas = json_payload['numero_semanas']
        self.id_usuario = json_payload['id_usuario']
        plan_entrenamiento = json_payload['plan_entrenamiento']
        self.lunes = plan_entrenamiento['lunes']
        self.martes = plan_entrenamiento['martes']
        self.miercoles = plan_entrenamiento['miercoles']
        self.jueves = plan_entrenamiento['jueves']
        self.viernes = plan_entrenamiento['viernes']
        self.sabado = plan_entrenamiento['sabado']
        self.domingo = plan_entrenamiento['domingo']

   # Función que realiza el registro del usuario en BD
    def registrar_plan_entrenamiento_bd(self):
        # Validar y eliminar si existe un plan de entrenamiento con el id_usaurio
        entrenamiento = Entrenamientos.query.filter_by(id_usuario=self.id_usuario).first()
        if entrenamiento:
            db.session.delete(entrenamiento)
            db.session.commit()
        
        # Registrar en BD
        entrenamiento = Entrenamientos(
            entrenamiento=self.entrenamiento, 
            numero_semanas=self.numero_semanas,
            id_usuario=self.id_usuario
        )
        plan_entrenamiento = PlanEntrenamiento(
            lunes=self.lunes,
            martes=self.martes,
            miercoles=self.miercoles,
            jueves=self.jueves,
            viernes=self.viernes,
            sabado=self.sabado,
            domingo=self.domingo
        )
        entrenamiento.plan_entrenamiento = plan_entrenamiento
        db.session.add(entrenamiento)
        db.session.commit()
        return entrenamiento

    # Función que retorna la recomendación de entrenamiento
    def execute(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            entrenamiento = self.registrar_plan_entrenamiento_bd()            
            return entrenamiento_schema.dump(entrenamiento)
        except IntegrityError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)
        except SQLAlchemyError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)