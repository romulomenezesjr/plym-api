from fastapi import APIRouter, Depends, HTTPException, status
from app.repository.users_repository import UsersRepository
from app.schemas import AccessToken
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils import utils, oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["auth"]
)

user_repo = UsersRepository()

@router.post("/login", response_model=AccessToken)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db) ):
    user_local = user_repo.getByEmail(user_credentials.username,db)
    if not user_local:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"user with email {user_credentials.username} not found" )
    
    if not utils.verify(user_credentials.password, user_local.password ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid password" )

    access_token = oauth2.create_access_token(data={"user_id": user_local.id})
    return {"access_token": access_token, "token_type":"bearer"}


