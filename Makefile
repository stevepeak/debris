.PHONY: watch test deploy

open:
	subl --project debris.sublime-project

watch:
	watchr Watch

p:
	. venv/bin/activate; python

test:
	. venv/bin/activate; pip uninstall -y debris
	. venv/bin/activate; python setup.py --quiet install
	psql debris -c "drop schema public;create schema public" -f tests/demo.sql
	. venv/bin/activate; nosetests --with-coverage --cover-package=debris --cover-html --cover-html-dir=htmlcov

update:
	. venv/bin/activate; pip install -r requirements.txt --upgrade

venv:
	virtualenv venv
	. venv/bin/activate; pip install -r requirements.txt
	psql -c "create database debris;"

deploy: tag upload

tag:
	git tag -a v$(shell python -c "import debris;print debris.version;") -m ""
	git push origin v$(shell python -c "import debris;print debris.version;")

upload:
	python setup.py sdist upload
