from pydantic import BaseModel


class Producto(BaseModel):
    nombre: str
    marca: str
    tipo_piel_id: int
    categoria_id: int


class Categoria(BaseModel):
    nombre: str


class Tipo_Piel(BaseModel):
    nombre: str
    descripcion: str