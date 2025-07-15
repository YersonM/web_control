from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from ..services.launcher import ejecutar_programa

router = APIRouter()

@router.get("/abrir/{programa}", response_class=PlainTextResponse)
async def abrir(programa: str):
    resultado = ejecutar_programa(programa)
    return resultado
