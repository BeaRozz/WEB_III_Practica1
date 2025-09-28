# app/routers/batch.py
from fastapi import APIRouter
from functools import reduce
from typing import List

# Importamos la lógica y modelos que vamos to reutilizar
from models import OperacionLote
from app.validation import ejecutar_validaciones

router = APIRouter()

@router.post("/batch")
def lote(operaciones: List[OperacionLote]):

    resultados_finales = []

    mapa_de_calculo = {
        "sum": lambda nums: sum(nums),
        "res": lambda nums: reduce(lambda x, y: x - y, nums),
        "mul": lambda nums: reduce(lambda x, y: x * y, nums),
        "div": lambda nums: reduce(lambda x, y: x / y, nums),
    }

    # Iteramos sobre cada operación que nos llegó en la lista
    for operacion in operaciones:
        error_dict = ejecutar_validaciones(operacion=operacion.op, nums=operacion.nums)

        if error_dict:
            resultados_finales.append(error_dict)
            continue

        funcion_de_calculo = mapa_de_calculo[operacion.op]
        resultado_calculo = funcion_de_calculo(operacion.nums)
        
        resultado_exitoso = {
            "operacion": operacion.op,
            "nums": operacion.nums,
            "resultado": resultado_calculo,
            "status": "success"
        }
        resultados_finales.append(resultado_exitoso)
    
    return {"resultados": resultados_finales}