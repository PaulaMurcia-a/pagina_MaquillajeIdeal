import psycopg2
import os



DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_YiocpP91Zqaz@ep-morning-cloud-aqy7nlua-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Crea las tablas si no existen."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tipos_piel (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL,
            marca VARCHAR(100) NOT NULL,
            tipo_piel_id INT REFERENCES tipos_piel(id),
            categoria_id INT REFERENCES categorias(id),
            estado VARCHAR(20) DEFAULT 'activo'
        );
    """)

    conn.commit()
    cur.close()
    conn.close()