.PHONY: help


help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# -- Application commands ---------------------------------------------------------- #
install:	## API - Install code dependencies
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Installing poetry..."
	@echo "# ----------------------------------------------------------------------- #"

	poetry install

	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Installing pre-commit hooks..."
	@echo "# ----------------------------------------------------------------------- #"

	poetry run pre-commit install

lint:	## API - Run the linter
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Running linter..."
	@echo "# ----------------------------------------------------------------------- #"

	poetry run pre-commit run $(if $(path),--files $(shell git ls-files $(path)),--all-files)

create-new-app:	## API - Create a new app
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Creating a new app:"
	@echo "# ----------------------------------------------------------------------- #"

	poetry run cookiecutter $(PWD)/src/libs/cookiecutter/create_app/ \
		--output-dir src/apps/

# -- Docker commands ---------------------------------------------------------- #
docker-build:	## Docker - Build the API
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Building the API image: (no-cache = $(if $(no-cache),true,false))"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml build $(if $(container),$(container),) $(if $(no-cache),--no-cache)

docker-up:	## Docker - Run the API
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Running the API container:"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml up -d $(if $(container),$(container),)

docker-down:	## Docker - Stop the API
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Stopping the API container:"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml down $(if $(container),$(container),)

docker-logs:	## Docker - Show the API container logs
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Showing the API container logs:"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml logs -f $(if $(container),$(container),)

docker-attach:	## Docker - Attach to the API container
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Attaching to the API container"
	@echo "» To exit, use Ctrl + C"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml attach $(if $(container),$(container),backend)

docker-exec:	## Docker - Execute a command in the API container
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Running command in the API container: $(if $(command),$(command),bash)"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml exec -it $(if $(container),$(container),backend) $(if $(command),$(command),sh)

recreate-dev:	## Docker - Recreate dev ambient
	make docker-down && \
	docker volume rm -f template_postgres_data && \
	make docker-build && \
	make docker-up env=dev && \
	make db-populate

recreate-prod:	## Docker - Recreate prod ambient
	make docker-build env=prod no-cache=y && \
	make docker-down containter="backend celery" && \
	make docker-up env=prod

# -- Database commands ---------------------------------------------------------- #
db-seed:	## Database - Seed the database with initial data
	make docker-exec command="python src/libs/database/seeds/__init__.py --seeds $(if $(seed),$(seed),all)"

db-populate:	## Database - Populate the database with initial data
	make db-migrate && \
	make db-seed

db-create-migration:	## Database - Create a new migration
	make docker-exec command="alembic revision --autogenerate -m '$(message)'"

db-merge-migrations:	## Database - Merge migrations
	make docker-exec command="alembic merge --message 'merge heads' heads"

db-migrate:	## Database - Deploy pending migrations
	make docker-exec command="alembic upgrade heads"

db-undo-migrate:	## Database - Undo the last migration
	make docker-exec command="alembic downgrade $(if $(rev),$(rev),-1)"

db-shell:	## Database - Open a database shell
	make docker-exec container="database" command="psql -U postgres -d dev"

# -- Testing commands ---------------------------------------------------------- #
test:	## Testing - Run the test suite
	make docker-exec command="coverage run -m unittest discover tests"
	make docker-exec command="coverage $(if $(only-report),report,xml)"