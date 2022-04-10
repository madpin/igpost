.ONESHELL:
.PHONY: env updated-deps

VENV = venv
ACTIVATE = $(VENV)/bin/activate
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SHELL := /bin/bash

## ----------------------------------------------------------------------
## Recipes to facilitate initial setup tasks, testing and running dags.
## "P" stands for 'Project', or the folder project name
## ----------------------------------------------------------------------
# SHELL := /bin/bash
.DEFAULT_GOAL := help

env_create2:	## env_create and installs
	## Example: env_create
	rm -rf $(VENV)
	python -m venv ./$(VENV)
	$(PIP) install -r requirements.in
	$(PIP) install -r requirements.dev.in

env_create:	## env_create
	## Example: env_create
	python -m venv ./$(VENV)

requirements:	## requirements
	$(PIP) install -r requirements.in

requirements_dev:	## env_create
	$(PIP) install -r requirements.dev.in

run:	## run
	$(PYTHON) ./src/
	
updated-deps:	## updated-deps
	source ./bash/make_func.sh && update_deps

pre-commit:	## pre-commit
	pre-commit

venv:	## venv
	source $(VENV)/bin/activate



help:	## Show this help
	@echo "Usage: make [target] ...\n"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//' | awk 'BEGIN {FS = "\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
