from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.schemas.task import TaskCreate, Task as TaskSchema, TaskUpdate
from app.routes.user import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Rota para CRIAR uma tarefa (Verifica se o projeto é do usuário)
@router.post("/", response_model=TaskSchema)
def create_task(
    task: TaskCreate, 
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verifica se o projeto existe e pertence ao usuário logado
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Você não tem permissão para adicionar tarefas a este projeto."
        )

    new_task = Task(**task.model_dump(), project_id=project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Rota para LISTAR todas as tarefas de um projeto (Apenas se o projeto for do usuário)
@router.get("/project/{project_id}", response_model=list[TaskSchema])
def list_project_tasks(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Primeiro checa se o projeto pertence ao usuário
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    return db.query(Task).filter(Task.project_id == project_id).all()

# Rota para ATUALIZAR uma tarefa (Ex: Marcar como concluída)
@router.put("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int, 
    task_data: TaskUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Busca a tarefa e faz um JOIN com Projeto para checar o dono
    db_task = db.query(Task).join(Project).filter(
        Task.id == task_id, 
        Project.owner_id == current_user.id
    ).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# Rota para DELETAR uma tarefa específica
@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Busca a tarefa garantindo que o dono do projeto é quem está logado
    db_task = db.query(Task).join(Project).filter(
        Task.id == task_id, 
        Project.owner_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(db_task)
    db.commit()
    return None