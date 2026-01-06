# Template API Project

FastAPI + SQLAlchemy starter tailored for microservices. Ships with authentication flows, SQLAdmin UI, background task plumbing, and dockerized local environments.

## Stack
- FastAPI app wiring and middlewares in [src/main.py](src/main.py#L1-L29)
- Configuration via `python-decouple` in [src/settings.py](src/settings.py#L1-L122)
- SQLAlchemy + Alembic session setup in [src/libs/database/session.py](src/libs/database/session.py#L1-L90)
- Auto-discovered versioned routers in [src/apps/__init__.py](src/apps/__init__.py#L1-L23)
- SQLAdmin console configured in [src/libs/admin/config.py](src/libs/admin/config.py#L1-L32)

## Features
- JWT auth endpoints for issuing, refreshing, and revoking tokens in [src/apps/auth/endpoints.py](src/apps/auth/endpoints.py#L1-L154)
- Built-in middlewares: DB session, CORS, request logging, profiling, localization (and JWT available but commented) loaded in [src/main.py](src/main.py#L7-L25)
- Cookiecutter scaffolding to generate new apps via `make create-new-app`
- Docker-first workflow with dev/prod compose files under `env/`
- Test suite with coverage and HTTPX helpers under `tests/`

## Project layout (key paths)
```
src/
	main.py                  # FastAPI app + middleware wiring
	settings.py              # Environment-driven settings
	apps/                    # Feature modules (auth, hc, roles, users, ...)
	libs/                    # Shared libs: admin, auth, db, locale, log, etc.
	tests/                   # Unit/integration tests
env/
	dev|prod/compose.yml     # Docker compose definitions
```

## Requirements
- Docker (for the provided workflows)
- Python 3.13+ and Poetry (if running locally without Docker)

## Quickstart
1) Copy and adjust environment variables
```
cp env/dev/.env.example env/dev/.env
```
Set database, Redis, JWT, email, and CORS values as needed (see [src/settings.py](src/settings.py#L7-L122) for the full list).

2) Install dependencies (local run)
```
make install
```

3) Run with Docker (recommended)
```
make build            # build dev images
make up               # start containers
make logs             # follow logs
make attach           # attach to backend container
```

4) Run locally without Docker (optional)
```
poetry run uvicorn src.main:app --reload
```

## Database
- Configure DB credentials in `.env` (dialect/user/pass/host/name).
- Apply migrations and seeds via make targets:
```
make db-migrate          # upgrade to latest
make db-create-migration message="add feature"
make db-seed             # run seeds
```

## Testing
```
make test                # runs coverage + unittest suite
```

## Creating a new app module
```
make create-new-app
```
This runs the cookiecutter template located at `src/libs/cookiecutter/create_app/` and drops a new module under `src/apps/` with routers auto-discovered by [src/apps/__init__.py](src/apps/__init__.py#L9-L23).

## Admin UI
- SQLAdmin is enabled with config in [src/libs/admin/config.py](src/libs/admin/config.py#L7-L32). Update branding (title/logo) or authentication backend there.

## Middlewares
- DB session (`DBMiddleware`), CORS, localization, logging, and profiling are enabled by default.
- JWT middleware is available but commented out in [src/main.py](src/main.py#L14-L21); uncomment when you want request-level auth checks.

## Make commands reference
```
make help                 # show targets
make install              # install deps + pre-commit
make lint                 # run pre-commit (ruff, etc.)
make build|up|down|logs   # docker lifecycle
make exec command="bash"  # exec into backend container
make db-*                 # migration helpers
make test                 # run tests with coverage
```
