from app.models import user, project, task
from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, project
from app.routes import user as user_routes
from app.routes import project as project_routes
from app.routes import task as task_routes
from fastapi.security import OAuth2PasswordBearer

# 1. Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# 2. Cria a instância do App
app = FastAPI(title="API de Gerenciamento Profissional")
# Isso diz ao Swagger que usaremos Tokens para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# 3. Rota de teste
@app.get("/")
def read_root():
    return {"status": "Online", "message": "Alicerce pronto!"}

# 4. Inclui as rotas (sempre depois de criar o 'app')
app.include_router(user_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)