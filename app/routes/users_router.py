from typing import List
from fastapi import status, HTTPException,Response, APIRouter, Depends
from app.repository.users_repository import UsersRepository
from app.utils import utils
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import  UserIn, UserOut, UserRole
from app.utils import oauth2

userRepo = UsersRepository()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code = status.HTTP_200_OK, response_model = List[UserOut])
def users(db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    """
    GET ALL
    """
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    users = userRepo.getAll(db)
    return users


@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = UserOut)
def get_user(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    """
    GET ID
    """
    local_user = userRepo.get(id, db)
    
    if not local_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found" )

    if user.role != UserRole.ADMIN or user.id != local_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

   
    return local_user

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    """
    POST USER
    """
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass

    if user.name is None:
        user.name = user.email

    new_user = userRepo.save(user, db)
    return new_user

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(id:int, user: UserIn, db: Session = Depends(get_db), logged_user = Depends(oauth2.get_current_user)):
    """
    UPDATE USER
    - Verifica se o id existe e lança 404 caso contrário
    - Atualiza o usuário correspondente
    """
    local_user = userRepo.get(id, db)
    if not local_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found" )

    if logged_user.role == UserRole.USER and local_user.id != logged_user.id:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"User id {logged_user.id} can not update user id {local_user.id}")

    updated_user = userRepo.update(local_user, user, db)
    return updated_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db: Session = Depends(get_db), logged_user = Depends(oauth2.get_current_user)):
    """
    DELETE USER
    - Verifica se o id existe e lança 404 caso contrário
    - Remove o usuário com id correspondente
    """
    local_user = userRepo.get(id, db)
    if not local_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found" )

    if logged_user.role == UserRole.USER and local_user.id != logged_user.id:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"User id {logged_user.id} can not delete user id {local_user.id}")

    userRepo.delete(local_user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)