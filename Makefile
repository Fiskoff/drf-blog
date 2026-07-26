MANAGE_PY ?= python manage.py

run:
	$(MANAGE_PY) runserver

makemigrations:
	$(MANAGE_PY) makemigrations

migrate:
	$(MANAGE_PY) migrate

freeze:
	pip freeze > requirements.txt

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt