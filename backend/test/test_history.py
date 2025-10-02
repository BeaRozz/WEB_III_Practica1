import pytest
import mongomock
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.routers import history

test_client = TestClient(app)

def test_obtener_historial_exitoso(monkeypatch):
    mock_collection = mongomock.MongoClient().practica1.historial
    
    operacion_de_prueba = {
        "operacion": "sum",
        "nums": [1, 1],
        "resultado": 2,
        "date": datetime.now(timezone.utc)
    }
    mock_collection.insert_one(operacion_de_prueba)

    monkeypatch.setattr(history, "collection_historial", mock_collection)

    response = test_client.get("/historial")

    assert response.status_code == 200
    
    response_data = response.json()
    assert "historial" in response_data
    assert len(response_data["historial"]) == 1

    resultado_api = response_data["historial"][0]
    
    assert resultado_api["operacion"] == operacion_de_prueba["operacion"]
    assert resultado_api["nums"] == operacion_de_prueba["nums"]
    assert resultado_api["resultado"] == operacion_de_prueba["resultado"]
    
    fecha_api = datetime.fromisoformat(resultado_api["date"])
    fecha_original_naive = operacion_de_prueba["date"].replace(tzinfo=None)
    assert abs(fecha_api - fecha_original_naive) < timedelta(seconds=1)


# Datos de prueba para filtros y ordenamientos
hoy = datetime.now(timezone.utc)
ayer = hoy - timedelta(days=1)
semana_pasada = hoy - timedelta(days=7)

datos_de_prueba_filtros = [
    {"operacion": "sum", "nums": [1, 1], "resultado": 2, "date": hoy},
    {"operacion": "div", "nums": [10, 2], "resultado": 5, "date": hoy - timedelta(seconds=1)},
    {"operacion": "sum", "nums": [3, 3], "resultado": 6, "date": ayer},
    {"operacion": "mul", "nums": [4, 4], "resultado": 16, "date": semana_pasada},
]

def to_comparable_set(documentos):
    return {
        (d['operacion'], tuple(d['nums']), d['resultado']) for d in documentos
    }

@pytest.mark.parametrize("url_filtro, indices_esperados", [
    ("?operacion=sum", [0, 2]),
    (f"?fecha_inicio={hoy.strftime('%Y-%m-%d')}", [0, 1]),
    (f"?fecha_inicio={ayer.strftime('%Y-%m-%d')}&fecha_fin={hoy.strftime('%Y-%m-%d')}", [0, 1, 2]),
    ("?orden=asc", [3, 2, 1, 0]),
    ("?operacion=sum&orden=asc", [2, 0]),
])
def test_historial_filtros_exitosos(monkeypatch, url_filtro, indices_esperados):

    mock_collection = mongomock.MongoClient().practica1.historial
    mock_collection.insert_many(datos_de_prueba_filtros)
    monkeypatch.setattr(history, "collection_historial", mock_collection)

    response = test_client.get(f"/historial{url_filtro}")

    assert response.status_code == 200

    documentos_esperados = [datos_de_prueba_filtros[i] for i in indices_esperados]
    response_data = response.json()["historial"]

    assert len(response_data) == len(documentos_esperados)

    if "orden=" in url_filtro:
        for i, item_esperado in enumerate(documentos_esperados):
            item_api = response_data[i]
            assert item_api["operacion"] == item_esperado["operacion"]
            assert item_api["nums"] == item_esperado["nums"]
            assert item_api["resultado"] == item_esperado["resultado"]
            fecha_api = datetime.fromisoformat(item_api["date"])
            fecha_esperada_naive = item_esperado["date"].replace(tzinfo=None)
            assert abs(fecha_api - fecha_esperada_naive) < timedelta(seconds=1)
    else:
        set_esperado = to_comparable_set(documentos_esperados)
        set_api = to_comparable_set(response_data)
        assert set_api == set_esperado



def test_historial_error_fecha_invalida():
    response = test_client.get("/historial?fecha_inicio=2025-10-01&fecha_fin=2025-09-30")
    assert response.status_code == 400
    expected_error = {
        "status_code": 400,
        "error": ["La fecha de inicio no puede ser posterior a la fecha de fin."]
    }
    assert response.json() == expected_error

@pytest.mark.parametrize("parametro, valor_invalido, mensaje_esperado", [
    (
        "operacion", 
        "resta", 
        "El tipo de operación 'resta' no es válido. Use uno de: ['sum', 'res', 'mul', 'div']"
    ),
    (
        "orden", 
        "aleatorio", 
        "El valor de orden 'aleatorio' no es válido. Use uno de: ['asc', 'desc']"
    ),
])
def test_historial_error_parametros_invalidos(parametro, valor_invalido, mensaje_esperado):
    response = test_client.get(f"/historial?{parametro}={valor_invalido}")
    assert response.status_code == 400
    expected_error = {
        "status_code": 400,
        "error": [mensaje_esperado]
    }
    assert response.json() == expected_error

