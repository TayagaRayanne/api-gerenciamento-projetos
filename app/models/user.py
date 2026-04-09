from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
# nos imports estou trazendo o 'Base' do SQLAlchemy, que é a classe base para os nossos modelos.
# O 'Column' é usado para definir as colunas da tabela, e os tipos como 'Integer', 'String' e 'Boolean' definem o tipo de dados de cada coluna.
# O 'User' é a classe que representa a tabela de usuários no banco de dados. Ela herda de 'Base', o que a torna um modelo do SQLAlchemy.

# Modelo de usuário para o banco de dados
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    projects = relationship("Project", back_populates="owner")  # Isso permite fazer o user.projects e receber uma lista de todos os projetos que pertencem a ele.

    # Aqui posso adicionar campos como 'cargo' ou 'departamento' futuramente