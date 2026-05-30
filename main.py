from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from contextlib import asynccontextmanager

from models import Producto, Categoria, TipoPiel
from database import init_db

from service import (
    get_productos,
    get_producto_by_id,
    create_producto,
    update_producto,
    delete_producto,
    cambiar_estado_producto,
    recomendar_productos,
    filtrar_productos,
    get_tipos_piel,
    buscar_tipo_piel,
    create_tipo_piel,
    update_tipo_piel,
    delete_tipo_piel,
    get_categorias,
    buscar_categoria,
    create_categoria,
    update_categoria,
    delete_categoria,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Beauty App",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    pieles = [
        {
            "nombre": "Piel Sensible",
            "imagen": "/static/img/piel-sensible.png",
            "descripcion": "Se irrita fácilmente, presenta enrojecimiento y reacciones a productos fuertes."
        },
        {
            "nombre": "Piel Seca",
            "imagen": "/static/img/piel-seca.png",
            "descripcion": "Se siente tirante, puede descamarse y necesita hidratación constante."
        },
        {
            "nombre": "Piel Grasosa",
            "imagen": "/static/img/piel-grasosa.png",
            "descripcion": "Presenta brillo visible, poros abiertos y tendencia a imperfecciones."
        },
        {
            "nombre": "Piel Mixta",
            "imagen": "/static/img/piel-mixta.png",
            "descripcion": "Zona T grasa y mejillas secas o normales."
        },
        {
            "nombre": "Piel Normal",
            "imagen": "/static/img/piel-normal.png",
            "descripcion": "Equilibrada, suave y sin exceso de brillo o resequedad."
        }
    ]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pieles": pieles
        }
    )
