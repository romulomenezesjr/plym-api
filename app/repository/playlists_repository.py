from sqlalchemy import func, outerjoin
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import PlaylistsDB
from app.models import PlaylistModel, LikedPlaylist
from .repository import Repository

class PlaylistsRepository(Repository):
      
    def getAll(self, db:Session, skip: int = 0, limit: int = 100):
        #db.query(PlaylistModel).offset(skip).limit(limit).all()
        playlists_with_like = db.query(
                            PlaylistModel, func.count(PlaylistModel.id).label("likes")
                        ).join(
                            LikedPlaylist, PlaylistModel.id == LikedPlaylist.playlist_id, isouter=True
                        ).group_by(
                            PlaylistModel.id
                        ).offset(skip).limit(limit)
        return playlists_with_like.all()
        
    
    def get(self, id: int, db:Session) -> PlaylistModel:
        #playlist = db.query(PlaylistModel).filter(PlaylistModel.id == id).first()
        playlist_with_like = db.query(
                    PlaylistModel, func.count(PlaylistModel.id).label("likes")
                    ).join(
                        LikedPlaylist, PlaylistModel.id == LikedPlaylist.playlist_id
                    ).group_by(
                        PlaylistModel.id
                    ).filter(
                        PlaylistModel.id == id
                    ).first()
        return playlist_with_like

    def save(self, playlist: PlaylistsDB, db:Session):
        db_content = PlaylistModel(**playlist.dict())
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content

    def update(self, content_model, content_data: PlaylistsDB, db:Session):
        content_model.title = content_data.title
        content_model.url = content_data.url
        db.commit()
        return content_model

    def delete(self, local_content, db:Session):
        db.delete(local_content)
        db.commit()

    def getByOwnerId(self, id, owner_id, db) -> PlaylistModel:
        return db.query(PlaylistModel).filter(PlaylistModel.owner_id == owner_id and PlaylistModel.id == id).first()