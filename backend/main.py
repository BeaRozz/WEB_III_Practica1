import datetime
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#MongoDB Colection
mongo_client = MongoClient("mongodb://admin_user:web3@practicas-mongo-1:27017/")
database = mongo_client.practica1
collection_historial = database.historial



#Una clase para controlarlos a todos, realmente gestiona todas las operaciones
class NumerosInput(BaseModel):
    nums: List[float]


#validaciones
def validar_no_negativos(nums: list[float]):
    if any(n < 0 for n in nums):
        return JSONResponse(
            status_code=400,
            content={
                "operacion": "sum",
                "nums": nums,
                "status_code": 400,
                "error": "No se permiten números negativos"
            }
        )

def validar_no_ceros(nums: list[float]):
    if any(n == 0 for n in nums):
        return JSONResponse(
            status_code=400,
            content={
                "operacion": "sum",
                "nums": nums,
                "status_code": 400,
                "error": "No se permiten ceros"
            }
        )

def validar_no_vacios(nums: list[float]):
    if not nums:
        return JSONResponse(
            status_code=400,
            content={
                "operacion": "sum",
                "nums": nums,
                "status_code": 400,
                "error": "Debe enviar al menos un número"
            }
        )

# --- Endpoint de suma ---
# --- Endpoint de suma (Usando el patrón de Retorno Temprano) ---
@app.post("/calculadora/sum")
def sumar_numeros(datos: NumerosInput):
    # Validaciones con retorno temprano
    error_vacio = validar_no_vacios(datos.nums)
    if error_vacio:
        return error_vacio

    error_negativo = validar_no_negativos(datos.nums)
    if error_negativo:
        return error_negativo

    error_cero = validar_no_ceros(datos.nums)
    if error_cero:
        return error_cero

    # Si llegamos aquí, no hubo errores. Este es el "camino feliz".
    resultado = sum(datos.nums)

    document = {
        "operacion": "sum",
        "nums": datos.nums,
        "resultado": resultado,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    collection_historial.insert_one(document)

    return {"nums": datos.nums, "resultado": resultado}


@app.get("/calculadora/historial")
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