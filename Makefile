.ONESHELL:
.PHONY: env updated-deps

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

## ----------------------------------------------------------------------
## Recipes to facilitate initial setup tasks, testing and running dags.
## "P" stands for 'Project', or the folder project name
## ----------------------------------------------------------------------
# SHELL := /bin/bash
.DEFAULT_GOAL := help

env_create:
	python -m venv ./$(VENV)

requirements:
	$(PIP) install -r requirements.in

requirements_dev:
	$(PIP) install -r requirements.dev.in

run:
	$(PYTHON) ./src/
	
updated-deps:
	source ./bash/make_func.sh && update_deps

pre-commit:
	pre-commit

# docker_run:	## Build and run using Docker
# 	## Example: make docker_run P="import_chs"
# 	touch .env
# 	source ./bash/bash_func.sh && docker_run

# bash_func:
# 	source ./bash/bash_func.sh && docker_run

# conda_create:	## Create and Activate the Conda Env
# 	conda create -n eda-magna python=3.9 -y

# py_run:	## Run from local python
# 	## Example: make py_run P="chs_calculation"
# 	source ./bash/bash_func.sh && py_run

# pre-commit:	## Run pre commit testings
# 	## Example: make pre-commit
# 	source ./bash/bash_func.sh && pre_commit

# update-deps:	## Run pip updates dependencies from master
# 	## Example: make update-deps
# 	## Example: make update-deps P="chs_calculation"
# 	./bash/update-deps.sh $(P)

# list-ps:	## List the valid Projects
# 	## Example: make list-dags
# 	source ./bash/bash_func.sh && list_ps

# cc_gbq_to_mysql:	## Example: make cc_gbq_to_mysql
# 	python $(PWD)/cookie_recipes/gbq_to_mysql/hooks/pre_call_cookiecutter.py
# 	cookiecutter $(PWD)/cookie_recipes/gbq_to_mysql

# cc_gbq_to_gbq:	## Example: make cc_gbq_to_mysql
# 	python $(PWD)/cookie_recipes/gbq_to_gbq/hooks/pre_call_cookiecutter.py
# 	cookiecutter $(PWD)/cookie_recipes/gbq_to_gbq


help:	## Show this help
	@echo "Usage: make [target] ...\n"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//' | awk 'BEGIN {FS = "\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
