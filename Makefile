DOCKER=$(shell which docker)
DOCKER-COMPOSE=$(shell which docker-compose)
PYTHON3=$(shell which python3)

help:
	@grep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

init: ## initialize environment
	$(DOCKER-COMPOSE) up -d flask_db
	$(DOCKER-COMPOSE) build
	$(DOCKER-COMPOSE) up flask_app

dbt: ## run dbt commands
	$(shell venv/bin/dbt seed --project-dir ./preston_ventures --profiles-dir ./preston_ventures)
	$(shell venv/bin/dbt run --project-dir ./preston_ventures --profiles-dir ./preston_ventures)
	$(shell venv/bin/dbt test --project-dir ./preston_ventures --profiles-dir ./preston_ventures)
