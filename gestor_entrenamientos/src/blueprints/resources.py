from flask import request, Blueprint
from commands.alertas import CrearAlerta
from commands.crear_plan_entrenamiento import CrearPlanEntrenamiento
from commands.registrar_resultados_entrenamiento import RegistrarResultadosEntrenamiento
from flask.json import jsonify
from queries.consultar_por_usuario import ConsultarPlanEntrenamientoPorUsuario

entrenamientos_blueprint = Blueprint(name='entrenamientos', import_name=__name__, url_prefix='/entrenamientos')

# Recurso que expone la funcionalidad healthcheck
@entrenamientos_blueprint.route('/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad notificacion de Alerta
@entrenamientos_blueprint.route('/alerta', methods=['POST'])
def notificacion_alerta():
    headers = request.headers
    data = request.get_json()
    return CrearAlerta(data, headers).execute()

# Recurso que expone la creación de plan de entrenamiento
@entrenamientos_blueprint.route('/plan-entrenamiento', methods=['POST'])
def crear_plan_entrenamiento():
    data = request.get_json()
    headers = request.headers
    plan_entrenamiento = CrearPlanEntrenamiento(data, headers).execute()
    return  jsonify(plan_entrenamiento)

# Recurso que expone consulta de plan de entrenamiento con base al id_usuario
@entrenamientos_blueprint.route('/plan-entrenamiento/usuario/<id_usuario>', methods=['GET'])
def consultar_plan_entrenamiento_por_usuario(id_usuario):
    headers = request.headers
    plan_entrenamiento = ConsultarPlanEntrenamientoPorUsuario(id_usuario, headers).query()
    return  jsonify(plan_entrenamiento)

# Recurso que expone la funcionalidad de registro de los resultados de entrenamiento
@entrenamientos_blueprint.route('/resultados-plan-entrenamiento', methods=['POST'])
def registrar_resultados_entrenamiento():
    headers = request.headers
    data = request.get_json()
    resultados_entrenamiento = RegistrarResultadosEntrenamiento(data, headers).execute()
    return jsonify(resultados_entrenamiento)