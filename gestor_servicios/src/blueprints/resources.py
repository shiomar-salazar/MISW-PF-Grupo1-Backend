from flask import request, Blueprint
from commands.notificaciones import CrearNotificaiconMasiva
from commands.registrar import RegistrarServicio 
from commands.agendar import AgendarServicio

servicios_blueprint = Blueprint('servicios', __name__)

# Recurso que expone la funcionalidad healthcheck
@servicios_blueprint.route('/servicios/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad notificacion Masiva
@servicios_blueprint.route('/servicios/notificacion', methods=['POST'])
def notificacion_masiva():
    headers = request.headers
    data = request.get_json()
    return CrearNotificaiconMasiva(data, headers).execute()

# Recurso que expone la funcionalidad registro de servicios
@servicios_blueprint.route('/servicios', methods=['POST'])
def registrar_servicio():
    data = request.get_json()
    headers = request.headers
    return RegistrarServicio(data, headers).execute()

# Recurso que expone la funcionalidad registro de servicios
@servicios_blueprint.route('/servicios/agendar', methods=['POST'])
def agendar_servicio():
    data = request.get_json()
    headers = request.headers
    return AgendarServicio(data, headers).execute()