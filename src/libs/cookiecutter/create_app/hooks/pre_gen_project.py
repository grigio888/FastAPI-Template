import re
import sys

app_name = '{{ cookiecutter.app_name }}'

if app_name == "" or len(app_name) < 3:
    print('[ERROR]: App name must be provided and be at least 3 characters long.')
    sys.exit(1)
