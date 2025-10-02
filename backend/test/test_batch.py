import pytest
import mongomock
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.routers import batch

test_client = TestClient(app)

# HAPPY PATH
def test_operaciones_basicas_happy_path():
    payload = [
        {"op": "sum", "nums": [10, 20, 5]},
        {"op": "mul", "nums": [5, 5, 5]}
    ]

    # Realizamos la petición a la API.
    response = test_client.post("/batch", json=payload)

    assert response.status_code == 200

    response_json = response.json()
    resultados = response_json.get("resultados", [])
    assert len(resultados) == 2

    # Veificar respuesta de la API
    assert resultados[0]["operacion"] == "sum"
    assert resultados[0]["resultado"] == 35
    assert resultados[0]["status"] == "success"

    assert resultados[1]["operacion"] == "mul"
    assert resultados[1]["resultado"] == 125
    assert resultados[1]["status"] == "success"




# NO HAPPY PATH
def test_operaciones_basicas_no_happy_path():
    payload = [
        {"op": "sum", "nums": [10, 20, 5]},
        {"op": "mul", "nums": [5, 5, -4]},
        {"op": "div", "nums": [100, 0]},
        {"op": "res", "nums": [50]},
    ]

    # Realizamos la petición a la API.
    response = test_client.post("/batch", json=payload)

    assert response.status_code == 200

    response_json = response.json()
    resultados = response_json.get("resultados", [])
    assert len(resultados) == 4

    # Veificar respuesta de la API
    assert resultados[0]["operacion"] == "sum"
    assert resultados[0]["resultado"] == 35
    assert resultados[0]["status"] == "success"

    assert resultados[1]["operacion"] == "mul"
    assert resultados[1]["status_code"] == 400
    assert resultados[1]["nums"] == [5, 5, -4]
    assert resultados[1]["error"] == ["No se permiten números negativos"]

    assert resultados[2]["operacion"] == "div"
    assert resultados[2]["status_code"] == 400
    assert resultados[2]["nums"] == [100, 0]
    assert resultados[2]["error"] == ["No se permiten ceros para esta operación"]

    assert resultados[3]["operacion"] == "res"
    assert resultados[3]["status_code"] == 400
    assert resultados[3]["nums"] == [50]
    assert resultados[3]["error"] == ["Debe enviar al menos dos números"]