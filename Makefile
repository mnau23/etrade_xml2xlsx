POETRY_RUN := poetry run

GREEN=\033[32;1m
NC=\033[0m # No Color

.PHONY: lint update clean help

lint: ## Autolinting code
	@echo "\n${GREEN}Linting files...${NC}\n"
	@${POETRY_RUN} black .
	@${POETRY_RUN} isort .
	@echo "\n${GREEN}Running bandit...${NC}\n"
	@${POETRY_RUN} bandit -c pyproject.toml -r src
	@echo "\n${GREEN}Running pylint...${NC}\n"
	@${POETRY_RUN} pylint src

update: ## Update the environment
	@echo "\n${GREEN}Showing current Python version on this project...${NC}\n"
	@${POETRY_RUN} python --version
	@echo "\n${GREEN}Updating the environment...${NC}\n"
	pip3 install --upgrade poetry
	poetry check
	@echo "\n${GREEN}Updating Poetry...${NC}\n"
	@${POETRY_RUN} pip install --upgrade pip setuptools
	poetry update
	@echo "\n${GREEN}Showing outdated packages...${NC}\n"
	@${POETRY_RUN} pip list -o --not-required --outdated

clean: ## Force a clean environment: remove all temporary files and cache
	@echo "\n${GREEN}Cleaning up...${NC}\n"
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	@echo "\n${GREEN}Removing Poetry environment...${NC}\n"
	poetry env list
	poetry env info -p
	poetry env remove $(shell poetry run which python)
	poetry env list

help: ## Show this help menu
	@egrep -h '\s##\s' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; \
		{printf "${GREEN}%-15s${NC}%s\n", $$1, $$2}'
