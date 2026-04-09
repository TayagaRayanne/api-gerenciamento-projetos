from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# endereço do banco de dados SQLite
# O "sqlite:///./" diz que o banco será um arquivo local chamado "sql_app.db" na raiz do projeto.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# O Engine: É quem conversa com o banco de dados.
# O 'connect_args' com 'check_same_thread: False' é uma exigência específica do SQLite 
# para permitir que o FastAPI acesse o banco com segurança.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal: É o fabricador de sessões do banco de dados. Cada vez que a API precisar ler ou salvar algo, ela vai pedir uma sessão para ela.
# autocommit=False garante que as mudanças só sejam salvas quando você der um 'db.commit()'. Isso é importante para evitar salvar mudanças acidentais :)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: É a classe base para os nossos modelos.
Base = declarative_base()

# Função para obter uma sessão do banco de dados.
def get_db():
    db = SessionLocal()
    try:
        yield db # Entrega a sessão para quem pediu (a rota da API),
    finally:
        db.close() # Fecha a sessão obrigatoriamente, mesmo se der erro no código.