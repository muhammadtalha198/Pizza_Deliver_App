# Pizza_Deliver_App
# python -m venv .venv
# source .venv/bin/activate
# deactivate

////-----------------------------------------------------------------------------------------
pip install -U pip
pip install -r requirements.txt
pip freeze > requirements.txt

////-----------------------------------------------------------------------------------------
# uvicorn app.main:app --reload



////-----------------------------------------------------------------------------------------
git commands 
# git checkout -b basic_feature
# git switch main

////-----------------------------------------------------------------------------------------
docker commands
# docker compose up -d
# docker exec -it pizza_db psql -U pizza -d pizza_delivery -c "\dt"

////-----------------------------------------------------------------------------------------


install alembic 
# alembic init alembic

A) Edit alembic.ini
Replace the URL line with:
# sqlalchemy.url = postgresql://pizza:pizza@localhost:5432/pizza_delivery

B) Update alembic/env.py
# from sqlmodel import SQLModel
# from app.models.user import User

Find:
# target_metadata = None
Replace:
# target_metadata = SQLModel.metadata

Generate migration:
# alembic revision --autogenerate -m "create users table"
# alembic upgrade head

alembic stamp head

////-----------------------------------------------------------------------------------------
test apis
# pytest -q


////-----------------------------------------------------------------------------------------