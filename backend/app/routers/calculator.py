# app/routers/calculator.py
import datetime
from fastapi import APIRouter
from functools import reduce

from models import NumerosInput
from database import collection_historial
from app.validation import ejecutar_validaciones

router = APIRouter()

# ----- OPERACIONES BÁSICAS -----
@router.post("/sum")
def suma(datos: NumerosInput):
    error_response = ejecutar_validaciones(operacion="sum", nums=datos.nums)
    if error_response:
        return error_response

    resultado = sum(datos.nums)

    document = {
        "operacion": "sum", "nums": datos.nums, "resultado": resultado,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    collection_historial.insert_one(document)
    return {"nums": datos.nums, "resultado": resultado}

@router.post("/res")
def resta(datos: NumerosInput):
    # Idéntica llamada a la validación
    error_response = ejecutar_validaciones(operacion="sub", nums=datos.nums)
    if error_response:
        return error_response

    resultado = reduce(lambda x, y: x - y, datos.nums)

    document = {
        "operacion": "sub", "nums": datos.nums, "resultado": resultado,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    collection_historial.insert_one(document)
    return {"nums": datos.nums, "resultado": resultado}

@router.post("/mul")
def multiplicacion(datos: NumerosInput):
    error_response = ejecutar_validaciones(operacion="mul", nums=datos.nums)
    if error_response:
        return error_response
    
    resultado = reduce(lambda x, y: x * y, datos.nums)

    document = {
        "operacion": "mul", "nums": datos.nums, "resultado": resultado,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    collection_historial.insert_one(document)
    return {"nums": datos.nums, "resultado": resultado}


@router.post("/div")
def division(datos: NumerosInput):
    error_response = ejecutar_validaciones(operacion="div", nums=datos.nums)
    if error_response:
        return error_response

    resultado = reduce(lambda x, y: x / y, datos.nums)

    document = {
        "operacion": "div", "nums": datos.nums, "resultado": resultado,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    collection_historial.insert_one(document)
    return {"nums": datos.nums, "resultado": resultado}