.PHONY: watch test deploy

open:
	subl --project debris.sublime-project

watch:
	watchr Watch

compare:
	hub compare $(shell heroku releases | grep Deploy | head -1 | python -c "import sys, re;print re.search('v\d+\s+Deploy\s+(\w+)', sys.stdin.read()).groups()[0]")...master

p:
	. venv/bin/activate; python

test:
	. venv/bin/activate; python -m unittest discover -s tests

update:
	. venv/bin/activate; pip install -r requirements.txt --upgrade

venv:
	virtualenv venv
	. venv/bin/activate; pip install -r requirements.txt