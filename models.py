from pydantic import BaseModel, field_validator
from typing import Optional


class Producto(BaseModel):
    nombre: str
    marca: str
    tipo_piel_id: int
    categoria_id: int

    
    @field_validator("nombre", "marca")
    @classmethod
    def no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()

    @field_validator("tipo_piel_id", "categoria_id")
    @classmethod
    def positivo(cls, v):
        if v <= 0:
            raise ValueError("El ID debe ser un número positivo")
        return v


class Categoria(BaseModel):
    nombre: str

    @field_validator("nombre")
    @classmethod
    def no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class TipoPiel(BaseModel):
    nombre: str
    descripcion: str

    @field_validator("nombre", "descripcion")
    @classmethod
    def no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()