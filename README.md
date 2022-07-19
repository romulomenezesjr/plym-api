# Objetivos
- Migrations with Alembic
- CORS
- GIT
- HEROKU

## Alembic
```
alembic init alembic
```
change the alembic env.py file inserting the Base.metadata and SQLALCHEMY_DATABASE_URL 

alembic revision --autogenerate -m "Auto generate"
alembic upgrade fffffff


## CORS


## GIT

## Heroku
 

Install heroku
sudo ln -s /var/lib/snapd/snap /snap
sudo snap install heroku --classic

Procfile
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
ADRIANO FALA DA FINAL CONTRA A ARGENTINA NA COPA AMÉRICA DE 2004 | Velozes Sports

```
$ heroku login
$ heroku create plym-api
```
Configure settings (.env) and mysql addon on heroku

```
$ git push heroku main
```


