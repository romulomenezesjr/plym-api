from typing import List
from fastapi import status, HTTPException,Response, APIRouter, Depends
from app.repository import playlists_repository, users_repository
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import  LikedPlaylists, Playlists, PlaylistsInput,PlaylistsDB
from app.utils import oauth2
from app.models import UserModel

playlistRepo = playlists_repository.PlaylistsRepository()
userRepo = users_repository.UsersRepository()

router = APIRouter(
    prefix="/playlists",
    tags=["playlists"],
    responses={404: {"description": "Not found"}},
)

#@router.get("/", status_code = status.HTTP_200_OK, response_model = List[Playlists])
@router.get("/", status_code = status.HTTP_200_OK, response_model = List[LikedPlaylists])
def contents(db: Session = Depends(get_db)):
    """
    GET ALL
    """
    return playlistRepo.getAll(db)

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = Playlists)
def get_playlist(id: int, db: Session = Depends(get_db)):
    """
    GET ID
    """
    content = playlistRepo.get(id, db)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist with id {id} not found" )
    return content

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = Playlists)
def create_content(playlist: PlaylistsInput, db: Session = Depends(get_db), user:UserModel = Depends(oauth2.get_current_user)):
    """
    POST CONTENT
    """
    playlist_db = PlaylistsDB(**playlist.dict(), owner_id=user.id)
    new_content = playlistRepo.save(playlist_db, db)
    
    return new_content

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Playlists)
def update_content(id:int, content: PlaylistsInput, db: Session = Depends(get_db), user:UserModel = Depends(oauth2.get_current_user)):
    """
    UPDATE PLAYLIST
    - Verifica se o id existe e lança 404 se não existe
    - Atualiza o conteúdo correspondente
    """
    local_playlist = playlistRepo.get(id, db)
    if not local_playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content with id {id} not found" )

    if local_playlist.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.email} doest owns playlist {local_playlist.title}")
    updated_content = playlistRepo.update(local_playlist, content, db)
    return updated_content

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(id:int,db: Session = Depends(get_db), user:UserModel = Depends(oauth2.get_current_user)):
    """
    DELETE PLAYLIST
    - Verifica se o id existe e lança 404 se não existe
    - Remove a playlist com id correspondente
    """
    local_playlist = playlistRepo.get(id, db)
    if not local_playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content with id {id} not found" )
    
    if local_playlist.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.email} doest owns playlist {local_playlist.title}")
        
    playlistRepo.delete(local_playlist, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
