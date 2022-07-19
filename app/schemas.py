from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, conint
from typing import Any, List, Optional, Union

#OAuth
class AccessToken(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

# User
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str]
    role: Optional[UserRole]

class UserIn(UserBase):
    password: str
    class Config:
        schema_extra = {
            "example": {
                "email": "romulo@gmail.com",
                "password": "remo",
                "name": "Romulo",
                "role": "user"
            }
        }
class UserOut(UserBase):
    id: int    
    created_at: datetime
    class Config:
        orm_mode = True

class UserDB(UserOut):
    password: str


## Playlist Schemas 
class PlaylistsBase(BaseModel):
    title: str
    thumbnail: str
    description: str
    favcount: int
    published: bool
    class Config:
        schema_extra = {
            "example": {
                "title": "Playlist ABC",
                "thumbnail": "https://www.spcdn.org/templates/sendpulsev1/img/sp_icons/sp-i-fb-autoposting.svg",
                "description": "Minha playlist",
                "favcount": 0,
                "published": True,
                #"user_id": 1
            }
        }

class PlaylistsDB(PlaylistsBase):
    owner_id: int

class PlaylistsInput(PlaylistsBase):
    pass

class Playlists(PlaylistsDB):
    id: int
    created_at: datetime
    owner: UserOut
    contents: List[Any]
    class Config:
        orm_mode = True

class LikedPlaylists(BaseModel):
    PlaylistModel: Playlists
    likes: int
    class Config:
        orm_mode = True

## Content Schemas 
class ContentBase(BaseModel):
    title: str
    url: str
    playlist_id:int
    class Config:
        schema_extra = {
            "example": {
                "title": "Video XZY",
                "url": "https://www.youtube.com/watch?v=4AVdTQ196cQ",
                "playlist_id": 1,
            }
        }

class ContentCreate(ContentBase):
    pass
   
class Content(ContentBase):
    id: int
    created_at: datetime
    #playlist: Playlists
    
    class Config:
        orm_mode = True

class Like(BaseModel):
    playlist_id: int
    user_id: int
    dir: conint(ge=0, le=1)