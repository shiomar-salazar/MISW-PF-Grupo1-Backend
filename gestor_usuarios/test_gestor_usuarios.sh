#!/bin/bash

####################################################################################################################################
echo "<================== [Inicio] Configuración ==================>"
TEST_PATH=tests-results-usuarios
mkdir -p $TEST_PATH
echo "Se realiza la creación del directorio [$TEST_PATH]"
MIN_COVERAGE=80
echo "La cobertura minima establecida para pasar las pruebas es [$MIN_COVERAGE]"
echo "<================== [Fin] Configuración ==================>"
echo "<================== [Inicio] instalacion de dependencias ==================>"
echo pwd
pip install -r gestor_usuarios/requirements.txt
echo "<================== [Fin][Exitoso] instalacion dependencias ==================>"
echo "<================== [Inicio] Ejecucion test ==================>"
pytest --cov-fail-under=80 --cov=src --cov-report=html:cov_report --junitxml=${SHORT_SHA}_usuarios__test_log.xml
echo "<================== [Fin][Exitoso] Ejecucion test ==================>"