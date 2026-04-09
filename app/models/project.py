from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    
    # ForeignKey liga este projeto a um ID de usuário
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Ponte para acessar o dono do projeto
    owner = relationship("User", back_populates="projects")
    
    # Adiciona o cascade para deletar tarefas órfãs quando um projeto for deletado
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")