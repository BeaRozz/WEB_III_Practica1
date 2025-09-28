from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database import collection_historial
from typing import Optional
from datetime import date, datetime, timedelta
from enum import Enum
import pymongo
from models import TipoOperacion, OrdenEnum

router = APIRouter()

@router.get("/historial")
def obtener_historial(
    operacion: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    orden: str = "desc"
):
    query = {}

    operaciones_validas = [item.value for item in TipoOperacion]
    if operacion and operacion not in operaciones_validas:
        error_body = {
            "status_code": 400,
            "error": [f"El tipo de operación '{operacion}' no es válido. Use uno de: {operaciones_validas}"]
        }
        return JSONResponse(status_code=400, content=error_body)
    
    ordenes_validos = [item.value for item in OrdenEnum]
    if orden not in ordenes_validos:
        error_body = {
            "status_code": 400,
            "error": [f"El valor de orden '{orden}' no es válido. Use uno de: {ordenes_validos}"]
        }
        return JSONResponse(status_code=400, content=error_body)
    
    if fecha_inicio and fecha_fin:
        if fecha_inicio > fecha_fin:
            error_body = {
                "status_code": 400,
                "error": ["La fecha de inicio no puede ser posterior a la fecha de fin."]
            }
            return JSONResponse(status_code=400, content=error_body)
    
    query = {}
    
    if operacion:
        query["operacion"] = operacion

    if fecha_inicio or fecha_fin:
        date_filter = {}
        if fecha_inicio:
            start_datetime = datetime.combine(fecha_inicio, datetime.min.time())
            date_filter["$gte"] = start_datetime
        if fecha_fin:
            end_datetime = datetime.combine(fecha_fin + timedelta(days=1), datetime.min.time())
            date_filter["$lt"] = end_datetime
        
        query["date"] = date_filter

    sort_order = pymongo.DESCENDING if orden == "desc" else pymongo.ASCENDING

    operaciones_cursor = collection_historial.find(query).sort("date", sort_order)

    historial = []
    for op in operaciones_cursor:
        historial.append({
            "operacion": op.get("operacion"),
            "nums": op.get("nums"),
            "resultado": op["resultado"],
            "date": op["date"].isoformat()
        })
    return {"historial": historial}