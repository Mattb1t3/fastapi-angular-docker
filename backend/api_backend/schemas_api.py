from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime

# Schema para registro
class UsuarioRegistro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6)
    confirmar_password: str = Field(..., min_length=6)
    
    @validator('confirmar_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return v
    
    @validator('nombre')
    def nombre_valido(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

# Schema para login
class UsuarioLogin(BaseModel):
    correo: EmailStr
    password: str

# Schema de respuesta de usuario
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str
    activo: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

# Schema de token
class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResponse

# Schema para datos del token
class TokenData(BaseModel):
    correo: Optional[str] = None
    rol: Optional[str] = None