from fastapi import FastAPI
from app.settings import settings
from app.database import Base, engine
from app.routes import contents_router,playlists_router, users_router, auth_router, likes_router
from fastapi.middleware.cors import CORSMiddleware
from app.utils import data_inicialization
# Criar as tabelas
Base.metadata.create_all(bind=engine)
#data_inicialization.data_load()

# Inicia a API
app = FastAPI(
    title = settings.api_title, 
    version = settings.api_version,
    description = settings.api_description,
    contact = { 
        "name" : settings.api_contact_name,
        "email" : settings.api_contact_email,
        "url" : settings.api_contact_url
        } 
    )

# Configura CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contents_router.router)
app.include_router(playlists_router.router)
app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(likes_router.router)