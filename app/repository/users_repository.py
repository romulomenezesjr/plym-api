from fastapi import HTTPException, status
from pydantic import EmailStr
from app.database import SessionLocal
from app.schemas import UserIn
from app.models import UserModel
from .repository import Repository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class UsersRepository(Repository):
    
    def getAll(self, db, skip: int = 0, limit: int = 100):
        return db.query(UserModel).offset(skip).limit(limit).all()
    
    def get(self, id: int, db):
        return db.query(UserModel).filter(UserModel.id == id).first()
    
    def getByEmail(self, email: EmailStr, db:Session):
        return db.query(UserModel).filter(UserModel.email == email).first()

    def save(self, user, db):
        db_user = UserModel(**user.dict())
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as err:           
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{err}" )

    # def update(self, id, schema_data: UserCreate):
    #     update_query = self.db.query(UserModel).filter(UserModel.id == id)
    #     update_query.update(schema_data.dict())
       
    #     self.db.commit()
    #     return update_query.first()

    def update(self, user_model:UserModel, schema_data: UserIn, db):
        user_model.email = schema_data.email
        user_model.password = schema_data.password
        db.commit()
        return user_model

    def delete(self, local_content, db):
        db.delete(local_content)
        db.commit()        