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
@app.get("/catalogo",
         response_class=HTMLResponse)
def catalogo(request: Request):

    productos = get_productos()

    return templates.TemplateResponse(
        "catalogo.html",
        {
            "request": request,
            "productos": productos
        }
    )
@app.get("/productos")
def listar():
    return get_productos()


@app.get("/productos/{producto_id}")
def obtener(producto_id: int):
    producto = get_producto_by_id(producto_id)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto


@app.post("/productos", status_code=201)
def crear(producto: Producto):

    try:

        new_id = create_producto(producto)

        return {
            "mensaje": "Producto creado",
            "id": new_id
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.put("/productos/{producto_id}")
def actualizar(producto_id: int, producto: Producto):

    if not update_producto(producto_id, producto):

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto actualizado"
    }


@app.delete("/productos/{producto_id}")
def eliminar(producto_id: int):

    if not delete_producto(producto_id):

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto desactivado"
    }


@app.put("/productos/{producto_id}/estado")
def cambiar_estado(producto_id: int, estado: str):

    resultado = cambiar_estado_producto(
        producto_id,
        estado
    )

    if resultado == "no_encontrado":

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    if resultado == "invalido":

        raise HTTPException(
            status_code=400,
            detail="Estado inválido. Use activo o inactivo"
        )

    if resultado == "igual":

        return {
            "mensaje": f"El producto ya está {estado}"
        }

    return {
        "mensaje": f"Estado cambiado a {estado}"
    }

@app.get("/productos/piel/{tipo_piel_id}")
def filtrar_piel(tipo_piel_id: int):
    return recomendar_productos(tipo_piel_id)


@app.get("/productos/marca/")
def filtrar(marca: str = None):
    return filtrar_productos(marca=marca)


@app.get("/productos/buscar/")
def buscar(nombre: str):
    return filtrar_productos(nombre=nombre)

@app.get("/tipos_piel")
def listar_tipos_piel():
    return get_tipos_piel()


@app.get("/tipos_piel/nombre/")
def buscar_tipo(nombre: str):
    return buscar_tipo_piel(nombre)


@app.post("/tipos_piel", status_code=201)
def crear_tipo(tipo: TipoPiel):

    new_id = create_tipo_piel(
        tipo.dict()
    )

    return {
        "mensaje": "Tipo de piel creado",
        "id": new_id
    }


@app.put("/tipos_piel/{tipo_id}")
def actualizar_tipo(tipo_id: int, tipo: TipoPiel):

    if not update_tipo_piel(
        tipo_id,
        tipo.dict()
    ):

        raise HTTPException(
            status_code=404,
            detail="No encontrado"
        )

    return {
        "mensaje": "Actualizado"
    }


@app.delete("/tipos_piel/{tipo_id}")
def eliminar_tipo(tipo_id: int):

    if not delete_tipo_piel(tipo_id):

        raise HTTPException(
            status_code=404,
            detail="No encontrado"
        )

    return {
        "mensaje": "Eliminado"
    }

@app.get("/categorias")
def listar_categorias():
    return get_categorias()


@app.get("/categorias/buscar/")
def buscar_cat(nombre: str):
    return buscar_categoria(nombre)


@app.post("/categorias", status_code=201)
def crear_categoria(categoria: Categoria):

    try:

        new_id = create_categoria(
            categoria.dict()
        )

        return {
            "mensaje": "Categoría creada",
            "id": new_id
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.put("/categorias/{cat_id}")
def actualizar_categoria(cat_id: int, categoria: Categoria):

    if not update_categoria(
        cat_id,
        categoria.dict()
    ):

        raise HTTPException(
            status_code=404,
            detail="No encontrada"
        )

    return {
        "mensaje": "Actualizada"
    }


@app.delete("/categorias/{cat_id}")
def eliminar_categoria(cat_id: int):

    if not delete_categoria(cat_id):

        raise HTTPException(
            status_code=404,
            detail="No encontrada"
        )

    return {
        "mensaje": "Eliminada"
    }