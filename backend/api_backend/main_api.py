from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ✅ DESPUÉS (correcto) - Imports relativos
from .database import engine, Base
from . import auth_api

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Usuarios",
    description="API con autenticación JWT para gestión de usuarios",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_api.router)

@app.get("/")
def root():
    return {
        "message": "API de Gestión de Usuarios",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}