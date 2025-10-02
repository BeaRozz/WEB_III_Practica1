import pytest
import mongomock
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.routers import calculator

test_client = TestClient(app)

# HAPPY PATH
@pytest.mark.parametrize("operacion, nums, resultado_esperado", [
    ("sum", [5, 10, 3], 18),
    ("res", [20, 5, 5], 10),
    ("mul", [2, 5, 10], 100),
    ("div", [100, 10, 2], 5),
    ("sum", [0, 0, 0], 0),
    ("res", [0, 0, 0], 0),
    ("mul", [1, 1, 1], 1),
    ("div", [1, 1, 1], 1),
    ("sum", [2.5, 2.5, 5.0], 10.0),
    ("res", [10.5, 5.5, 2.0], 3.0),
    ("mul", [2.5, 4.0, 2.0], 20.0),
    ("div", [20.0, 4.0, 2.0], 2.5),
    ("sum", [6, 7, 8, 9, 1, 3], 34),
    ("res", [100, 12, 23, 56, 1], 8),
    ("mul", [8, 3, 6, 9, 5, 3, 4], 77760),
    ("div", [40, 2, 1, 5, 2], 2)
])
def test_operaciones_basicas_happy_path(monkeypatch, operacion, nums, resultado_esperado):
    # Simulamos la base de datos.
    mock_collection = mongomock.MongoClient().practica1.historial
    monkeypatch.setattr(calculator, "collection_historial", mock_collection)

    # Realizamos la petición a la API.
    response = test_client.post(
        f"/calculadora/{operacion}",
        json={"nums": nums}
    )

    # Veificar respuesta de la API
    assert response.status_code == 200
    assert response.json() == {"nums": nums, "resultado": resultado_esperado}

    # Verificar guardado
    documento_guardado = mock_collection.find_one({"operacion": operacion, "resultado": resultado_esperado})
    assert documento_guardado is not None
    assert documento_guardado["nums"] == nums


# NO HAPPY PATH
@pytest.mark.parametrize("operacion, nums_invalidos, error_esperado", [
    ("sum", [5], ["Debe enviar al menos dos números"]),
    ("res", [-10, 5], ["No se permiten números negativos"]),
    ("div", [100, 0], ["No se permiten ceros para esta operación"]),
    ("mul", [5, -5, 0], ["No se permiten números negativos"] ),
    ("div", [10, 2, -1], ["No se permiten números negativos"]),
    ("sum", [], ["Debe enviar al menos dos números"]),
    ("res", [0], ["Debe enviar al menos dos números"]),
    ("mul", [1], ["Debe enviar al menos dos números"]),
    ("div", [1], ["Debe enviar al menos dos números"]),
    ("sum", [-1, -2, -3], ["No se permiten números negativos"]),
    ("res", [-5, -10], ["No se permiten números negativos"]),
    ("mul", [-2, -3, -4], ["No se permiten números negativos"]),
    ("div", [-10, -2], ["No se permiten números negativos"]),
    ("div", [10, -0, 2], ["No se permiten ceros para esta operación"]),
    ("div", [0, -10, 2], ["No se permiten números negativos", "No se permiten ceros para esta operación"]),
    ("mul", [-3], ["Debe enviar al menos dos números", "No se permiten números negativos"])
])
def test_operaciones_basicas_error_path(monkeypatch, operacion, nums_invalidos, error_esperado):
    # Simulamos la base de datos.
    mock_collection = mongomock.MongoClient().practica1.historial
    monkeypatch.setattr(calculator, "collection_historial", mock_collection)


    # Realizamos la petición a la API.
    response = test_client.post(
        f"/calculadora/{operacion}",
        json={"nums": nums_invalidos}
    )

    # Verificar respuesta de la API
    assert response.status_code == 400
    expected_error = {
        "operacion": operacion,
        "nums": nums_invalidos,
        "status_code": 400,
        "error": error_esperado
    }
    assert response.json() == expected_error
    
    # Verificar que no se guardó
    documento_guardado = mock_collection.find_one({"operacion": operacion, "nums": nums_invalidos})
    assert documento_guardado is None

