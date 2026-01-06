"""
Celery - Configuration module.
"""

import json

from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.utilities.path import load_all_objects_from

log = get_logger()


task_serializer: str = "json"
accept_content: list[str] = ["json"]  # Ignore other content types
result_serializer: str = "json"
timezone: str = "Europe/Lisbon"
enable_utc: bool = True

# In here, we should import the tasks that we want to schedule
all_imports = load_all_objects_from("tasks", "imports", as_list=True) or []

imports: list[str] = []
for item in all_imports:
    imports.extend(item)

# In here, we should define the schedule for the tasks
all_beat_schedule = load_all_objects_from("tasks", "beat_schedule", as_list=True) or {}

beat_schedule: dict[str, dict] = {}
for item in all_beat_schedule:
    beat_schedule.update(item)

log.info(f"{_()}: # --------------------------- CELERY --------------------------- #")
log.info(f"{_()}: Celery configuration loaded.")
log.info(f"{_()}: Imports: {json.dumps(imports, indent=4)}")
log.info(f"{_()}: Beat schedule: {json.dumps(beat_schedule, indent=4, default=str)}")
log.info(f"{_()}: # -------------------------------------------------------------- #")
