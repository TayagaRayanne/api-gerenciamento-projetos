from pydantic import BaseModel
from typing import Optional

# Aqui é definido os esquemas para as tarefas, seguindo a mesma lógica dos usuários e projetos. O TaskBase tem os campos comuns, o TaskCreate é para quando criamos uma tarefa, e o Task é para quando a API devolve uma tarefa (incluindo o ID e o ID do projeto a que pertence).
class TaskBase(BaseModel):
    description: str
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True # Isso permite que o Pydantic leia dados do SQLAlchemy e converta para o formato do esquema.

# Aqui defini o esquema para atualização de tarefas, onde tudo é opcional, 
# permitindo que o usuário envie apenas os campos que deseja atualizar.
class TaskUpdate(BaseModel):
    description: Optional[str] = None
    is_completed: Optional[bool] = None