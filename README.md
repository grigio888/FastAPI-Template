# Template API Project

---

# About

This is a template API for a microservice that can be used as a starting point for new projects.


## Dependencies

- Docker


## Contains

- Python3.13+
- Poetry
- Makefile


## Before you start

Make sure you have Docker installed and running on your machine.

## Structure

### File Structure

The project is structured as follows:

...

### Middlewares

`Authorization`
- The main responsibility of the `authorization` middleware is to check if the user is authenticated. If the user is not authenticated, the middleware will return a `401 Unauthorized` response.

- It is important to note that the `authorization` middleware is not responsible to log the user in, it is only responsible to check if the user is authenticated.

- It protects all routes inside the microservice by default, unless the route is explicitly passed in `EXCLUDED_PATHS` on the `.env` file (accepts regex).

`CORS`

- Simple CORS middleware that allows everything by default.

- `ALLOWED_ORIGINS`, `ALLOWED_METHODS` and `ALLOWED_HEADERS` can be configured in the `.env` file.

# Make commands

```
make attach                         Run the API
make build                          Build the API
make help                           Display this help
make install                        Install the API dependencies
make run                            Run the API
```
