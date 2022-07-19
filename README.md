# Objetivos
- Migrations with Alembic
- CORS

## Alembic
```
alembic init alembic
```
change the alembic env.py file inserting the Base.metadata and SQLALCHEMY_DATABASE_URL 

alembic revision --autogenerate -m "Auto generate"
alembic upgrade fffffff


## CORS
