# app/routers/history.py
from fastapi import APIRouter
from database import collection_historial

# El resto del archivo se queda exactamente igual...
router = APIRouter()

@router.get("/historial")
def obtener_historial():
    operaciones = collection_historial.find({})
    historial = []
    for operacion in operaciones:
        historial.append({
            "operacion": operacion.get("operacion"),
            "nums": operacion.get("nums"),
            "resultado": operacion["resultado"],
            "date": operacion["date"].isoformat()
        })
    return {"historial": historial}