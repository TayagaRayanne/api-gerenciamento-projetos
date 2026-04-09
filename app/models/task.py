from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Modelo de tarefa para o banco de dados (uma tarefa pertence a um projeto, e um projeto pode ter várias tarefas)
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    
    # A chave que liga a Tarefa ao Projeto
    project_id = Column(Integer, ForeignKey("projects.id"))

    # Relacionamento inverso: a tarefa sabe qual é o seu projeto
    project = relationship("Project", back_populates="tasks")