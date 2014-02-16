.PHONY: watch test deploy

open:
	subl --project debris.sublime-project

watch:
	watchr Watch

p:
	. venv/bin/activate; python

test:
	. venv/bin/activate; python -m unittest discover -s tests/2

update:
	. venv/bin/activate; pip install -r requirements.txt --upgrade

venv:
	virtualenv venv
	. venv/bin/activate; pip install -r requirements.txt

deploy: tag upload

tag:
	git tag -a v$(shell python -c "import debris;print debris.version;") -m ""
	git push origin v$(shell python -c "import debris;print debris.version;")

upload:
	python setup.py sdist upload
