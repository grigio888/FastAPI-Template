"""
Alembic relation of models.
"""

from importlib import import_module
from pathlib import Path

from src.libs.database.base_model import BaseModel
from src.libs.log import get_context as _
from src.libs.log import get_logger

log = get_logger()


def get_project_root(marker: str = "src") -> Path:
    """
    Get the root folder of the project.
    """

    log.debug(f"alembic.{_()}: Getting project root with marker: {marker}")

    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / marker).exists():
            log.debug(f"alembic.{_()}: Found project root: {parent}")
            return parent

    message = f"Could not find project root with marker: {marker}"
    log.error(f"alembic.{_()}: {message}")
    raise FileNotFoundError(message)


def find_models_modules(apps_path: Path) -> list[Path]:
    """
    Find all models modules in the given apps path.

    Args:
        apps_path (str): The path to the apps directory.

    Returns:
        list: A list of module names that contain models.

    """

    log.debug(f"alembic.{_()}: Finding models modules in: {apps_path}")

    models_modules = []

    for app in apps_path.iterdir():
        log.debug(f"alembic.{_()}: Checking app: {app}")

        if not app.is_dir():
            continue

        if (app / "models").exists() and (app / "models").is_dir():
            models_modules.append(app / "models")

        elif (app / "models.py").exists():
            models_modules.append(app / "models.py")

    log.debug(f"alembic.{_()}: Found models modules: {models_modules}")

    return models_modules


def import_path(module: Path) -> str:
    """Convert a Path object to a module import path."""

    absolute_path = module.as_posix()

    relative_path = "src" + absolute_path.split("src")[-1]

    python_path = relative_path.replace(".py", "").replace("/", ".")

    return python_path.lstrip(".")


def import_models_module(models_module: Path) -> object:
    """
    Import all models modules.

    Args:
        models_module (Path): The module path to import.

    """

    if not models_module.exists():
        log.error(f"alembic.{_()}: Models module does not exist: {models_module}")
        return None

    if models_module.is_dir() and not (models_module / "__init__.py").exists():
        log.error(
            f"alembic.{_()}: Models module directory does not contain "
            f"__init__.py: {models_module}",
        )
        return None

    import_path_str = import_path(models_module)
    log.debug(f"alembic.{_()}: Importing module: {import_path_str}")

    try:
        return import_module(import_path_str)
    except Exception:
        log.exception(f"alembic.{_()}: Failed to import module: {import_path_str}")
        return None


def import_models_from_module(module: object) -> list[type[BaseModel]]:
    """
    Import all models from a given module.

    Args:
        module: The module to import models from.

    Returns:
        list: A list of imported model classes.

    """

    log.debug(f"alembic.{_()}: Importing models from module: {module}")

    models = []

    for name in dir(module):
        if name.startswith("_") or name == "BaseModel":
            continue

        obj = getattr(module, name)

        if not isinstance(obj, type):
            continue

        log.debug(f"alembic.{_()}: Found model: {name}")
        models.append(obj)

    return models


APPS_PATH = get_project_root() / "src" / "apps"

models_modules = find_models_modules(APPS_PATH)


for models_module in models_modules:
    log.debug(f"alembic.{_()}: Importing models module: {models_module}")
    module = import_models_module(models_module)

    if module:
        models = import_models_from_module(module)

        if not models:
            log.debug(f"alembic.{_()}: No models found in module: {module}")
            continue

        for model in models:
            log.debug(f"alembic.{_()}: Registering model: {model.__name__}")
            globals()[model.__name__] = model
