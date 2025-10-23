from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from .deps_api import get_db, get_current_user
from .models import Usuario
from .schemas_api import UsuarioRegistro, UsuarioLogin, Token, UsuarioResponse
from .config_api import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/registro", response_model=Token, status_code=status.HTTP_201_CREATED)
def registro(usuario_data: UsuarioRegistro, db: Session = Depends(get_db)):
    """Registra un nuevo usuario"""
    
    # Verificar si el correo ya existe
    usuario_existente = db.query(Usuario).filter(
        Usuario.correo == usuario_data.correo
    ).first()
    
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        correo=usuario_data.correo,
        password_hash=get_password_hash(usuario_data.password),
        rol="user"  # Por defecto es usuario
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": nuevo_usuario.correo, "rol": nuevo_usuario.rol},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": UsuarioResponse.from_orm(nuevo_usuario)
    }

@router.post("/login", response_model=Token)
def login(usuario_data: UsuarioLogin, db: Session = Depends(get_db)):
    """Inicia sesión de usuario"""
    
    # Buscar usuario por correo
    usuario = db.query(Usuario).filter(
        Usuario.correo == usuario_data.correo
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(usuario_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    # Verificar si está activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacta al administrador"
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.correo, "rol": usuario.rol},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": UsuarioResponse.from_orm(usuario)
    }

@router.get("/me", response_model=UsuarioResponse)
async def obtener_usuario_actual(
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene información del usuario actual"""
    return UsuarioResponse.from_orm(current_user)

@router.post("/logout")
async def logout():
    """Cierra sesión (el cliente debe eliminar el token)"""
    return {"message": "Sesión cerrada exitosamente"}