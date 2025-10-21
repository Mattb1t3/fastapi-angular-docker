# 🚀 Proyecto Full Stack: FastAPI + Angular + Docker

Aplicación web desarrollada con **FastAPI (Python 3.10)**, **Angular 16**, **MySQL**, y **Docker Compose** sobre **WSL2 (Ubuntu)**.

---

## 📂 Estructura del Proyecto

project-root/
├── backend/
│ ├── api_backend/
│ │ ├── main_api.py
│ │ ├── config_api.py
│ │ ├── models_api.py
│ │ ├── schemas_api.py
│ │ ├── crud_api.py
│ │ ├── deps_api.py
│ │ ├── routers_api/
│ │ │ ├── auth_router.py
│ │ │ ├── users_router.py
│ │ │ └── upload_router.py
│ │ └── servicios_api/
│ │ └── procesador_excel.py
│ ├── Dockerfile_backend
│ ├── requirements_backend.txt
│ └── alembic_backend/
│
├── frontend/
│ ├── src_frontend/
│ │ └── app_frontend/
│ │ ├── services_frontend/
│ │ │ ├── api_service.ts
│ │ │ └── auth_service.ts
│ │ ├── components_login/
│ │ ├── components_register/
│ │ ├── components_users/
│ │ └── components_bulk_upload/
│ ├── Dockerfile_frontend
│ └── package.json
│
├── docker-compose.yml
├── .env
└── README.md


---

## ⚙️ Tecnologías Utilizadas

- **Backend:** FastAPI (Python 3.10)
- **Frontend:** Angular 16 (Node 20)
- **Base de Datos:** MySQL
- **Contenedores:** Docker + Docker Compose v2
- **Entorno:** WSL2 (Ubuntu)
- **Editor:** Visual Studio Code

---

## 🧰 Comandos de Uso

### 🔹 Construir y levantar contenedores
```bash
docker compose up --build

🔹 Detener contenedores
docker compose down

🔹 Ver logs
docker compose logs -f

🌐 Flujo de Comunicación entre Contenedores (Docker Compose)

La aplicación se levanta con 3 contenedores principales:

Servicio	Función	Puerto Expuesto	Se comunica con
backend	API REST en FastAPI	8000	base_datos, frontend
frontend	Aplicación Angular	4200	backend
base_datos	MySQL	3306	backend

Todos los servicios comparten una red interna de Docker (creada automáticamente por docker-compose), por lo que se comunican usando los nombres de servicio definidos en docker-compose.yml.

Ejemplo dentro del backend (FastAPI):

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://appuser:apppass@base_datos:3306/app_db"


Ejemplo dentro del frontend (Angular):

export const environment = {
  apiUrl: 'http://backend:8000'
};


El frontend se comunica con el backend usando el nombre backend dentro de la red interna,
pero desde el navegador local el acceso es:

Frontend → http://localhost:4200
Backend → http://localhost:8000

🧪 Variables de Entorno (.env)

Ejemplo del archivo .env:

MYSQL_ROOT_PASSWORD=rootpass
MYSQL_DATABASE=app_db
MYSQL_USER=appuser
MYSQL_PASSWORD=apppass


Estas variables se cargan automáticamente en el docker-compose.yml.

🗂️ Archivos Clave
Archivo	Descripción
Dockerfile_backend	Imagen para FastAPI (instala dependencias y ejecuta Uvicorn)
Dockerfile_frontend	Imagen para Angular (compila y sirve con nginx o dev server)
docker-compose.yml	Orquestación de todos los servicios (red, volumenes, puertos)
.env	Variables de entorno para la base de datos
requirements_backend.txt	Dependencias del backend
package.json	Dependencias del frontend