from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import status, HTTPException,Response, APIRouter, Depends
from app.database import get_db
from app.schemas import ContentCreate, Content
from app.repository import contents_repository, playlists_repository
from app.utils import oauth2

contents_repo = contents_repository.ContentRepository()
playlists_repo = playlists_repository.PlaylistsRepository()

router = APIRouter(
    prefix="/contents",
    tags=["contents"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code = status.HTTP_200_OK, response_model = List[Content])
def contents(db: Session = Depends(get_db),  skip: int= 0, limit: int = 5, search: Optional[str]=""):
    """
    GET ALL
    """
    limit = limit if limit < 100 else 100
    return contents_repo.getAll(db,  skip, limit, search)

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = Content)
def get_content(id: int, db: Session = Depends(get_db)):
    """
    GET ID
    """
    content = contents_repo.get(id, db)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content with id {id} not found" )
    return content

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = Content)
def create_content(content: ContentCreate, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    """
    POST CONTENT
    """
    playlist = playlists_repo.getByOwnerId(content.playlist_id, user.id, db)
    if playlist.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


    new_content = contents_repo.save(content,db)
    
    return new_content

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Content)
def update_content(id:int, content: ContentCreate, db: Session = Depends(get_db)):
    """
    UPDATE CONTENT
    - Verifica se o id existe e lança 404 se não existe
    - Atualiza o conteúdo correspondente
    """
    local_content = contents_repo.get(id,db)
    if not local_content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content with id {id} not found" )
    updated_content = contents_repo.update(local_content,content,db)
    return updated_content

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_content(id:int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    """
    DELETE CONTENT
    - Verifica se o id existe e lança 404 se não existe
    - Remove o conteúdo com id correspondente
    """
    local_content = contents_repo.get(id,db)
    if not local_content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content with id {id} not found" )
    contents_repo.delete(local_content,db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

