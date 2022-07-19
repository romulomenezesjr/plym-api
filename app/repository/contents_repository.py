from typing import Optional
from sqlalchemy.orm import Session
from app.schemas import ContentCreate
from app.models import ContentModel
from app.repository.repository import Repository

class ContentRepository(Repository):
    
    def __init__(self):
        pass
    
    def getAll(self, db:Session, skip: int = 0, limit: int = 100, search: Optional[str]=""):
       contents_query = db.query(ContentModel).filter(ContentModel.title.contains(search)).offset(skip).limit(limit)       
       contents = contents_query.all()
       return contents
    
    def get(self, id: int, db:Session):
        return db.query(ContentModel).filter(ContentModel.id == id).first()
    
    def getByTitle(self, title: str, db:Session):
        return db.query(ContentModel).filter(ContentModel.title == title).all()

    def save(self, content, db:Session):
        db_content = ContentModel(**content.dict())
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content

    def update(self, content_model, content_data: ContentCreate,db:Session):
        content_model.title = content_data.title
        content_model.url = content_data.url
        db.commit()
        return content_model

    def delete(self, local_content,db:Session):
        db.delete(local_content)
        db.commit()        