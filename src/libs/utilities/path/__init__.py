"""
Utilities - Path.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path


def get_project_root(marker: str = "src") -> Path:
    """
    # Get the root folder of the project.

    ---

    Usage:
    ```python
    from src.libs.utilities.path import get_project_root

    project_root = get_project_root()
    # "/path/to/project/root"
    ```
    """

    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / marker).exists():
            return parent

    message = f"Could not find project root with marker: {marker}"
    raise FileNotFoundError(message)


sys.path.append(str(get_project_root()))


from importlib import import_module  # noqa: E402

from src.libs.log import get_context as _  # noqa: E402
from src.libs.log import get_logger  # noqa: E402

log = get_logger()


def find_modules(
    apps_path: Path,
    target: str,
) -> list[Path]:
    """
    # Find all modules in the given apps path.

    Args:
        apps_path (str): The path to the apps directory.
        target (str): The target directory name to search for.

    Returns:
        list: A list of module names that contain models.

    """

    modules: list[Path] = []
    seen: set[str] = set()

    # Find directories named `target` recursively
    for d in apps_path.rglob(target):
        try:
            if d.is_dir():
                resolved = str(d.resolve())
                if resolved not in seen:
                    modules.append(d)
                    seen.add(resolved)
        except Exception:
            log.exception(f"{_()}: Error accessing directory.")
            continue

    # Find files named `target.py` recursively
    for f in apps_path.rglob(f"{target}.py"):
        try:
            if f.is_file():
                resolved = str(f.resolve())
                if resolved not in seen:
                    modules.append(f)
                    seen.add(resolved)
        except Exception:
            log.exception(f"{_()}: Error accessing file.")
            continue

    return modules


def import_path(
    module: Path,
) -> str:
    """Convert a Path object to a module import path."""

    absolute_path = module.as_posix()

    relative_path = "src" + absolute_path.split("src")[-1]

    python_path = relative_path.replace(".py", "").replace("/", ".")

    return python_path.lstrip(".")


def import_all_modules(
    module: Path,
) -> object:
    """
    Import all modules.

    Args:
        module (Path): The module path to import.

    """

    if not module.exists():
        log.error(f"{_()}: Module does not exist: {module}")
        return None

    if module.is_dir() and not (module / "__init__.py").exists():
        log.error(
            f"{_()}: Module directory does not contain __init__.py: {module}",
        )
        return None

    import_path_str = import_path(module)

    try:
        return import_module(import_path_str)
    except Exception:
        log.exception(f"{_()}: Failed to import module: {import_path_str}")
        return None


def import_objects_from_module(
    module: object,
    type_of: str | type | tuple[type, ...] | None = None,
) -> list:
    """
    Import all objects of a given type from a given module.

    Args:
        module: The module to import objects from.
        type_of: The type of objects to import.

    Returns:
        list: A list of imported objects.

    """

    objects = []
    to_ignore = ["BaseModel", "DeclarativeBaseModel", "ModelView", "CustomModelView"]

    for name in dir(module):
        is_priv_attrs = name.startswith("_")
        is_in_ignore = name in to_ignore
        is_type_of_string = (
            type_of
            and isinstance(type_of, str)
            and (type_of in name or type_of == name)
        )

        obj = getattr(module, name)

        is_type_of_object = (
            type_of and not isinstance(type_of, str) and isinstance(obj, type_of)
        )

        if (
            is_priv_attrs
            or is_in_ignore
            or (not is_type_of_string and not is_type_of_object)
        ):
            continue

        objects.append(obj)

    return objects


def load_all_objects_from(  # type: ignore[return]
    module_name: str,
    type_of: str | type | tuple[type, ...] | None = None,
    as_list: bool = False,
    only_modules: bool = False,
    order: list[Callable | bool | None] | None = None,
) -> list | None:
    """
    Load all objects from the specified module and type.

    Args:
        module_name (str): The name of the module to load.
        type_of (str): The type of objects to load.
        as_list (bool): If True, return a list of objects instead of setting them
            in globals.
        only_modules (bool): If True, return only the modules without importing them.
        order (list): A list containing a callable for sorting and a boolean for reverse
            sorting.

    """

    apps_path = get_project_root() / "src" / "apps"
    scraper_path = get_project_root() / "src" / "scrapers"

    models_modules = find_modules(apps_path, module_name)
    models_modules += find_modules(scraper_path, module_name)

    relation = []

    for models_module in models_modules:
        module = import_all_modules(models_module)

        if not module:
            log.error(
                f"{_()}: Failed to import module: {models_module}",
            )

        if only_modules:
            relation.append(module)
            continue

        models = import_objects_from_module(module, type_of=type_of)

        if not models:
            continue

        relation.extend(models)

    if order:
        key: Callable | None = None

        if len(order) > 0 and callable(order[0]):
            key = order[0]

        reverse = bool(order[1]) if len(order) > 1 else False

        relation.sort(key=key, reverse=reverse)

    if as_list or only_modules:
        return relation

    log.debug(f"{_()}: Importing objects: {[model.__name__ for model in relation]}")  # type: ignore[attr-defined]

    for model in relation:  # noqa: RET503
        model_name = str(getattr(model, "__name__", model))

        globals()[model_name] = model


if __name__ == "__main__":
    items = load_all_objects_from(
        "endpoints",
        "router",
        as_list=True,
        order=[lambda x: x.tags[0] if x.tags else "", False],
    )
