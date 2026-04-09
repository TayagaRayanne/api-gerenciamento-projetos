from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, Project as ProjectSchema, ProjectUpdate
from app.routes.user import get_current_user
from app.models.user import User
from sqlalchemy import func

router = APIRouter(prefix="/projects", tags=["Projects"])

# Rota para CRIAR um projeto (vincula automaticamente ao usuário logado)
@router.post("/", response_model=ProjectSchema)
def create_project(
    project: ProjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # O owner_id é preenchido automaticamente com o ID de quem está logado
    new_project = Project(**project.model_dump(), owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# Rota para LISTAR apenas os projetos do usuário logado
@router.get("/", response_model=list[ProjectSchema])
def list_projects(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(Project).filter(Project.owner_id == current_user.id).all()

# Rota para BUSCAR um projeto específico (apenas se pertencer ao usuário)
@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return project

# Rota para EDITAR um projeto (apenas se pertencer ao usuário)
@router.put("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int, 
    project_data: ProjectUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    update_data = project_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

# Rota para DELETAR um projeto (apenas se pertencer ao usuário)
@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db.delete(project)
    db.commit()
    return None

# Rota para obter um resumo do progresso dos projetos do usuário
@router.get("/dashboard/summary")
def get_project_summary(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Busca os projetos do usuário
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    
    summary = []
    
    for project in projects:
        total_tasks = len(project.tasks)
        # Conta quantas tarefas estão marcadas como is_completed = True
        completed_tasks = sum(1 for task in project.tasks if task.is_completed)
        
        # Cálculo da porcentagem (evitando divisão por zero)
        percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        summary.append({
            "project_id": project.id,
            "title": project.title,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress": f"{round(percentage, 2)}%"
        })
    
    return summary