import math
from typing import Optional, List, Callable
from fastapi.responses import JSONResponse

# --- Reglas de validación individuales ---

def validar_no_negativos(nums: list[float]) -> Optional[str]:
    if any(math.copysign(1.0, n) == -1.0 for n in nums):
        return "No se permiten números negativos"
    return None

def validar_no_ceros(nums: list[float]) -> Optional[str]:
    if any(n == 0 for n in nums):
        return "No se permiten ceros para esta operación"
    return None

def validar_numeros_minimos(nums: list[float]) -> Optional[str]:
    if len(nums) < 2:
        return "Debe enviar al menos dos números"
    return None


# --- Conjunto de Reglas Estándar ---

def obtener_reglas_aritmeticas_estandar() -> list:
    return [validar_numeros_minimos, validar_no_negativos]


# --- Función Orquestadora "Inteligente" (sin cambios) ---

def ejecutar_validaciones(operacion: str, nums: List[float]) -> Optional[dict]:

    reglas_a_aplicar = obtener_reglas_aritmeticas_estandar()
    
    if operacion == "div":
        reglas_a_aplicar.append(validar_no_ceros)
        
    lista_de_errores = []
    for regla_func in reglas_a_aplicar:
        error = regla_func(nums)
        if error:
            lista_de_errores.append(error)
            
    if lista_de_errores:
        error_body = {
            "operacion": operacion, "nums": nums,
            "status_code": 400, "error": lista_de_errores
        }
        return error_body
        
    return None