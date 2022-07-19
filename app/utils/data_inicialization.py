from app.database import get_db
from app.models import UserModel, ContentModel, PlaylistModel
from app.utils import utils

users = [
    {
    "id": 1000,
    "email": "admin@admin.com",
    "password": utils.hash ("admin"),
    "name": "Admin",
    "role" : "admin"
    },
     {
    "id": 1,
    "email": "user@user.com",
    "password": utils.hash ("user"),
    "name": "User",
    "role" : "user"
    },
]

playlists = [
    {
        "id": 1000,
        "title": "First playlist",
        "description": "Description of the first playlist added",
        "thumbnail": "",
        "favcount": 0,
        "published": True,
        "owner_id" : 1000,
    }
]

contents = [
    {
        "id": 1001,
        "title": "First content on first playlist",
        "url": "nourl",
        "playlist_id": 1000
    },
    {
        "id": 1002,
        "title": "First content on first playlist",
        "url": "nourl",
        "playlist_id": 1000
    },
    {
        "id": 1003,
        "title": "First content on first playlist",
        "url": "nourl",
        "playlist_id": 1000
    },
    {
        "id": 1004,
        "title": "First content on first playlist",
        "url": "nourl",
        "playlist_id": 1000
    }
]

def data_load(delete_on_startup = False):   
    db = next(get_db())
    
    if len(db.query(UserModel).all()) == 0:
        try:
            for user in users:
                db.add(UserModel(**user))
                db.commit()
                db.refresh(user)    
        except Exception as err:   
            print(err)        
            db.rollback()

    if len(db.query(PlaylistModel).all()) == 0:
        try:
            for playlist in playlists:
                db.add(PlaylistModel(**playlist))
                db.commit()
                db.refresh(playlist)    
        except Exception as err:   
            print(err)        
            db.rollback()

    if len(db.query(ContentModel).all()) == 0:
        try:
            for content in contents:
                db.add(ContentModel(**content))
                db.commit()
                db.refresh(content)    
        except Exception as err:   
            print(err)        
            db.rollback()


from app.database import engine
from sqlalchemy import text
def script_load():
    with engine.connect() as con:
        with open("app/utils/query.sql", "r") as file:
            for line in file:
                query = text(line)
                try:
                    con.execute(query)
                except Exception as err:
                    print(err)


