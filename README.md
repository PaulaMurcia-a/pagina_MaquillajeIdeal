#  Beauty Ideal

Sistema web para la gestión y recomendación de productos de maquillaje según el tipo de piel del usuario.

---

##  Descripción

Beauty Ideal es una aplicación web desarrollada para ayudar a los usuarios a identificar su tipo de piel y encontrar productos de maquillaje adecuados para sus características.

El sistema permite administrar un catálogo de productos organizados por categorías y tipos de piel, facilitando la búsqueda y recomendación de productos cosméticos.

---

##  Objetivos

- Identificar los diferentes tipos de piel.
- Recomendar productos adecuados para cada tipo de piel.
- Gestionar productos de maquillaje mediante operaciones CRUD.
- Organizar productos por categorías.
- Almacenar información en una base de datos PostgreSQL alojada en Neon.

---

##  Tecnologías Utilizadas

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend
- Python
- FastAPI

### Base de Datos
- PostgreSQL
- Neon Database

### Herramientas
- Git
- GitHub
- PyCharm

---

##  Estructura del Proyecto

```text
BeautyAPP_pagina/
│
├── static/
│   ├── img/
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── catalogo.html
│   └── estadisticas.html
│
├── .env
├── .gitignore
├── database.py
├── main.py
├── models.py
├── service.py
├── requirements.txt
├── README.md
```

---

## ️ Funcionalidades

### Gestión de Productos

 Crear productos

 Consultar productos

 Eliminar productos

 Filtrar productos por categoría

 Filtrar productos por tipo de piel

### Gestión de Categorías

 Consultar categorías

### Gestión de Tipos de Piel

 Consultar tipos de piel

 Mostrar descripción de cada tipo de piel

### Dashboard

 Visualización de estadísticas mediante gráficos

 Información organizada para facilitar la toma de decisiones

### Recomendaciones

 Recomendación de productos según el tipo de piel

---

##  Base de Datos

### Tabla: tipos_piel

| Campo | Tipo |
|---------|---------|
| id | INTEGER |
| nombre | VARCHAR |
| descripcion | TEXT |

### Tabla: categorias

| Campo | Tipo |
|---------|---------|
| id | INTEGER |
| nombre | VARCHAR |

### Tabla: productos

| Campo | Tipo |
|---------|---------|
| id | INTEGER |
| nombre | VARCHAR |
| marca | VARCHAR |
| tipo_piel_id | INTEGER |
| categoria_id | INTEGER |

---

## Diagrama Entidad Relación

```mermaid
erDiagram

PRODUCTOS {
    int id PK
    string nombre
    string marca
    int tipo_piel_id FK
    int categoria_id FK
}

TIPOS_PIEL {
    int id PK
    string nombre
    string descripcion
}

CATEGORIAS {
    int id PK
    string nombre
}

TIPOS_PIEL ||--o{ PRODUCTOS : recomienda
CATEGORIAS ||--o{ PRODUCTOS : clasifica
```

---

##  Diagrama UML

```mermaid
classDiagram

class Producto{
    +id:int
    +nombre:string
    +marca:string
    +tipo_piel_id:int
    +categoria_id:int
}

class Categoria{
    +id:int
    +nombre:string
}

class TipoPiel{
    +id:int
    +nombre:string
    +descripcion:string
}

Producto --> Categoria
Producto --> TipoPiel
```

---

## Arquitectura del Sistema

```mermaid
flowchart TD

A[Usuario] --> B[Frontend<br>HTML, CSS, JS]
B --> C[Backend<br>FastAPI]
C --> D[Service.py]
D --> E[Database.py]
E --> F[(Neon PostgreSQL)]
```

---

##  Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/BeautyIdeal.git
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crear archivo `.env` con la conexión a Neon:

```env
DATABASE_URL=postgresql://usuario:password@host/database
```

### 6. Ejecutar el proyecto


```bash
uvicorn main:app --reload
```

---

##  Autora

**Paula Mariyey Murcia Sánchez**

Proyecto académico desarrollado para la gestión y recomendación de productos de maquillaje según el tipo de piel.

---

##  Licencia

Proyecto desarrollado con fines académicos.

