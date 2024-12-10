.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:	## Build project with compose
	docker compose build

.PHONY: up
up:	## Run project with compose
	docker compose up --remove-orphans

.PHONY: clean
clean: ## Clean Reset project containers and volumes with compose
	docker compose down -v --remove-orphans | true
	docker compose rm -f | true
	docker volume rm flota_db_data | true

.PHONY: migrate-apply
migrate-apply: ## apply alembic migrations to database/schema
	docker compose run --rm app alembic upgrade head

.PHONY: feed_users
feed_users: ## create database objects and insert data
	docker compose exec db psql aws_service user -f /home/gx/code/users.sql | true