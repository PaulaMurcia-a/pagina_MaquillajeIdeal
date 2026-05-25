from database import get_connection
from models import Producto


# PRODUCTOS


def get_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, marca, tipo_piel_id, categoria_id, estado FROM productos WHERE estado = 'activo'")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [_producto_row(r) for r in rows]


def get_producto_by_id(producto_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nombre, marca, tipo_piel_id, categoria_id, estado FROM productos WHERE id = %s AND estado = 'activo'",
        (producto_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return _producto_row(row) if row else None


def create_producto(producto: Producto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO productos (nombre, marca, tipo_piel_id, categoria_id, estado) VALUES (%s, %s, %s, %s, 'activo') RETURNING id",
        (producto.nombre, producto.marca, producto.tipo_piel_id, producto.categoria_id)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


def update_producto(producto_id: int, updated: Producto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE productos SET nombre=%s, marca=%s, tipo_piel_id=%s, categoria_id=%s WHERE id=%s",
        (updated.nombre, updated.marca, updated.tipo_piel_id, updated.categoria_id, producto_id)
    )
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return affected > 0


def cambiar_estado_producto(producto_id: int, estado: str):
    if estado not in ("activo", "inactivo"):
        return "invalido"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT estado FROM productos WHERE id = %s", (producto_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return "no_encontrado"

    if row[0] == estado:
        cur.close()
        conn.close()
        return "igual"

    cur.execute("UPDATE productos SET estado=%s WHERE id=%s", (estado, producto_id))
    conn.commit()
    cur.close()
    conn.close()
    return "actualizado"


def delete_producto(producto_id: int):
    """Soft delete: cambia estado a inactivo."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE productos SET estado='inactivo' WHERE id=%s AND estado='activo'", (producto_id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return affected > 0

# FILTROS


def recomendar_productos(tipo_piel_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nombre, marca, tipo_piel_id, categoria_id, estado FROM productos WHERE tipo_piel_id=%s AND estado='activo'",
        (tipo_piel_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [_producto_row(r) for r in rows]


def filtrar_productos(nombre: str = None, marca: str = None):
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT id, nombre, marca, tipo_piel_id, categoria_id, estado FROM productos WHERE estado='activo'"
    params = []

    if nombre:
        query += " AND LOWER(nombre) LIKE %s"
        params.append(f"%{nombre.lower()}%")

    if marca:
        query += " AND LOWER(marca) LIKE %s"
        params.append(f"%{marca.lower()}%")

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [_producto_row(r) for r in rows]

# TIPOS DE PIEL

def get_tipos_piel():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, descripcion FROM tipos_piel")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "descripcion": r[2]} for r in rows]


def buscar_tipo_piel(nombre: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nombre, descripcion FROM tipos_piel WHERE LOWER(nombre) LIKE %s",
        (f"%{nombre.lower()}%",)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "descripcion": r[2]} for r in rows]


def create_tipo_piel(tipo: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tipos_piel (nombre, descripcion) VALUES (%s, %s) RETURNING id",
        (tipo["nombre"], tipo["descripcion"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


def update_tipo_piel(tipo_id: int, updated: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tipos_piel SET nombre=%s, descripcion=%s WHERE id=%s",
        (updated["nombre"], updated["descripcion"], tipo_id)
    )
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return affected > 0


def delete_tipo_piel(tipo_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tipos_piel WHERE id=%s", (tipo_id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return affected > 0


# CATEGORÍAS


def get_categorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM categorias")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1]} for r in rows]


def buscar_categoria(nombre: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nombre FROM categorias WHERE LOWER(nombre) LIKE %s",
        (f"%{nombre.lower()}%",)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1]} for r in rows]


def create_categoria(categoria: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM categorias WHERE LOWER(nombre) = LOWER(%s)", (categoria["nombre"],))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise ValueError("Ya existe una categoría con ese nombre")

    cur.execute(
        "INSERT INTO categorias (nombre) VALUES (%s) RETURNING id",
        (categoria["nombre"],)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


def update_categoria(cat_id: int, updated: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE categorias SET nombre=%s WHERE id=%s", (updated["nombre"], cat_id))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return affected > 0


def delete_categoria(cat_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM categorias WHERE id=%s", (cat_id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return affected > 0


def _producto_row(r):
    return {
        "id": r[0],
        "nombre": r[1],
        "marca": r[2],
        "tipo_piel_id": r[3],
        "categoria_id": r[4],
        "estado": r[5],
    }