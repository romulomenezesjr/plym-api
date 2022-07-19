from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    api_title: str
    api_version: str
    api_description:str
    api_contact_name:str
    api_contact_email: str
    api_contact_url: str
    api_terms: str
    api_licence: str

    jwt_algorithm:str
    jwt_secret_key:str
    jwt_exp_time: int
    
    class Config:
        env_file = ".env"


settings = Settings()