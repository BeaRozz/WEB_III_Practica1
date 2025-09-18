import pytest
import mongomock

from pytest import monkeypatch
from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.testclient import TestClient

import main

client = TestClient(app)
mongo_client = mongomock.MongoClient()
database = mongo_client.practica1
collection_historial = database.historial

@pytest.mark.parametrize(
        "numeroa, numerob, resultado",
        [
            (5, 10, 15),
            (0, 0, 0),
            (-5, 5, 0),
            (-10, -5, -15),
            (2.5, 2.5, 5.0),
            (10, -20, -10)
        ]
)

def test_sumar(monkeypatch, numeroa, numerob, resultado):
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get(f"/calculadora/sum?a={numeroa}&b={numerob}")
    assert response.status_code == 200
    assert response.json() == {"a": numeroa, "b": numerob, "resultado": resultado}
    
    assert collection_historial.find_one({"resultado": resultado, "a": numeroa, "b": numerob}) is not None