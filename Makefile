.PHONY: help


help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install the API dependencies
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Installing poetry..."
	@echo "# ----------------------------------------------------------------------- #"

	poetry install

	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Installing pre-commit hooks..."
	@echo "# ----------------------------------------------------------------------- #"

	poetry run pre-commit install

build: ## Build the API
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Building the API image: (no-cache = $(if $(no-cache),true,false))"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml build $(if $(no-cache),--no-cache)

up: ## Run the API
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Running the API container:"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml up $(if $(cont),$(cont),backend) -d

down: ## Stop the API
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Stopping the API container:"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml down $(if $(cont),$(cont),backend) -d

logs: ## Show the API container logs
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Showing the API container logs:"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml logs -f $(if $(cont),$(cont),backend)

attach: ## Run the API
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Attaching to the API container"
	@echo "» To exit, use Ctrl + C"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml attach $(if $(cont),$(cont),backend)

exec: ## Execute a command in the API container
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Running command in the API container: $(if $(command),$(command),bash)"
	@echo "# ----------------------------------------------------------------------- #"

	docker compose -f env/$(if $(strip $(env)),$(env)/,dev/)compose.yml exec -it $(if $(cont),$(cont),backend) $(if $(command),$(command),sh)

lint:
	@echo "# ----------------------------------------------------------------------- #"
	@echo "» Running linter..."
	@echo "# ----------------------------------------------------------------------- #"

	poetry run pre-commit run --all-files

recreate-dev: ## Recreate dev ambient
	make build && make up env=dev

create-migration: ## Create a new migration
	make exec command="alembic revision --autogenerate -m '$(message)'"

migrate: ## Deploy pending migrations
	make exec command="alembic upgrade heads"

test:
	make exec command="coverage run -m unittest discover tests"
	make exec command="coverage $(if $(only-report),report,xml)"
