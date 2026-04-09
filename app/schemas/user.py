from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema base para um usuário (sem a senha, que é sensível)
class UserBase(BaseModel):
    full_name: str
    email: EmailStr

# Esquema para quando alguém estiver criando um usuário (precisa da senha)
class UserCreate(UserBase):
    password: str

# Esquema para quando a API devolver um usuário (não devolve a senha por segurança!)
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True # Isso permite que o Pydantic leia dados do SQLAlchemy e converta para o formato do esquema.
        
# Esquema para os dados que chegam no Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str