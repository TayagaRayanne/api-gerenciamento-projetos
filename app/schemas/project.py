from pydantic import BaseModel
from typing import Optional

# Esquema base com o que é comum ao projeto
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

# Esquema para criação (o que o usuário envia)
class ProjectCreate(ProjectBase):
    pass

# Esquema para leitura (o que a API devolve, incluindo o ID e o dono)
class Project(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True # Isso permite que o Pydantic leia dados do SQLAlchemy e converta para o formato do esquema.
        
# Esquema para o que pode ser editado (tudo é opcional aqui)
class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None