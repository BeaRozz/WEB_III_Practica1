from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos los routers desde la carpeta app/routers
from app.routers import calculator, history, batch

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(calculator.router, prefix="/calculadora", tags=["Calculadora"])
app.include_router(history.router, tags=["Historial"])
app.include_router(batch.router, tags=["Procesamiento por Lote"])

@app.get("/")
def read_root():
    return {"message": "¿Qué haces aquí?"}