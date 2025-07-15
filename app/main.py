import subprocess
import urllib.parse
from fastapi import FastAPI, Request, Form, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import database
from pathlib import Path



app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    apps = database.listar_apps_activas()
    return templates.TemplateResponse("index.html", {"request": request, "apps": apps})


@app.get("/abrir/{ruta}")
async def abrir_app(ruta: str):
    ruta_decodificada = urllib.parse.unquote(ruta)

    try:
        if "!" in ruta_decodificada:
            # Es una app instalada desde la Microsoft Store
            print(f"Abriendo app instalada desde la Microsoft Store: {ruta_decodificada}")
            comando = f'start "" shell:AppsFolder\\{ruta_decodificada}'
            subprocess.Popen(comando, shell=True)
        else:
            # Ruta tradicional de archivo ejecutable
            print(f"Abriendo app tradicional: {ruta_decodificada}")
            comando = f'"{ruta_decodificada}"'
            subprocess.Popen(comando, shell=True)

        return {"mensaje": f"Ejecutando: {ruta_decodificada}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mantenedorApp", response_class=HTMLResponse)
async def mantenedor_app(request: Request):
    apps = database.listar_apps()
    edit_id = request.cookies.get("edit_id")
    app_edit = database.obtener_app(int(edit_id)) if edit_id else None
    response = templates.TemplateResponse("mantenedorApp.html", {"request": request, "apps": apps, "edit_app": app_edit})
    
    # Borrar cookie después de mostrar el formulario de edición
    if edit_id:
        response.delete_cookie("edit_id")
    return response

@app.post("/mantenedorApp")
async def manejar_formulario(
    request: Request,
    response: Response,
    action: str = Form(...),
    id: int = Form(None),
    name: str = Form(None),
    route: str = Form(None),
    status: int = Form(None),
):
    if action == "agregar":
        database.agregar_app(name, route, status)
    elif action == "actualizar" and id is not None:
        database.actualizar_app(id, name, route, status)
    elif action == "eliminar" and id is not None:
        database.eliminar_app(id)
    elif action == "editar" and id is not None:
        redirect = RedirectResponse("/mantenedorApp", status_code=303)
        redirect.set_cookie(key="edit_id", value=str(id))
        return redirect

    return RedirectResponse(url="/mantenedorApp", status_code=303)
