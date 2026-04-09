import bcrypt

# Essa função recebe a senha pura, transforma em bytes, gera um "sal" (uma string aleatória que é adicionada à senha para aumentar a segurança) e depois gera o hash da senha usando o bcrypt.
# O resultado é decodificado de volta para string para ser salvo no banco de dados.
def get_password_hash(password: str) -> str:
    # Transforma a string em bytes
    pwd_bytes = password.encode('utf-8')
    # Gera o "sal" e o hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Retorna como string para salvar no banco
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compara a senha digitada com o hash do banco, ou seja, verifica se a senha digitada, quando transformada em hash, é igual ao hash armazenado.
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )
    
from datetime import datetime, timedelta, timezone
from jose import jwt

# CHAVE SECRETA e ALGORITMO para criar e verificar os tokens JWT (JSON Web Tokens), que são usados para autenticação.
SECRET_KEY = "sua_chave_secreta_super_poderosa_e_longa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # O token vale por 30 minutos

def create_access_token(data: dict):
    to_encode = data.copy()
    # Define quando o token vai expirar
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Gera o código criptografado (o Token)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt