from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas
from fastapi.security import OAuth2PasswordBearer
from app.repository.users_repository import UsersRepository
from app.settings import settings
from app.database import get_db
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_exp_time

def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id = payload.get("user_id")
        
        if not id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    token =  verify_access_token(token)    
    user_repo = UsersRepository()    
    return user_repo.get(token.id, next(get_db()))