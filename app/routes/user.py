from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, UserLogin
from app.core.security import get_password_hash
from app.core.security import verify_password
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

# Cria o roteador para organizar as rotas de usuários
router = APIRouter(prefix="/users", tags=["Users"])

# 1. Rota de Criação de Usuário (POST)
@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user # O return precisa ficar dentro da função onde ele foi criado!

# 2. Rota para DELETAR um usuário específico pelo ID (DELETE)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == user_id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado."
        )

    user_query.delete(synchronize_session=False)
    db.commit()
    return None

# 3. Rota de Login (Autenticação)
@router.post("/login")
# Mudamos 'UserLogin' para 'OAuth2PasswordRequestForm = Depends()'
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # O OAuth2PasswordRequestForm usa 'username' em vez de 'email' por padrão
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )

    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")    
# Essa função é o "segurança" que confere o crachá e diz quem é a pessoa
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Abrimos o token usando nossa chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user