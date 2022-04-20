import yaml
from pathlib import Path

from nameless_server import logger_config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open(f'{BASE_DIR}/system/environments.yaml', 'r') as f:
    ENVIRONMENT = yaml.load(f, Loader=yaml.FullLoader)

with open(f'{BASE_DIR}/system/keys.yaml', 'r') as f:
    KEYS = yaml.load(f, Loader=yaml.FullLoader)


# Internationalization
LANGUAGE_CODE = ENVIRONMENT['settings']['language']
TIME_ZONE = ENVIRONMENT['settings']['timezone']


# Logger setting
LOGGER_CONFIG = logger_config.get_logging_config(
    project_name=ENVIRONMENT['server']['name'],
    log_dir=(BASE_DIR / ENVIRONMENT['settings']['log_dir'])
)

LOG_FILES = [
    BASE_DIR / f"{LOGGER_CONFIG['handlers']['debug']['filename']}",
    BASE_DIR / f"{LOGGER_CONFIG['handlers']['request_handler']['filename']}"
]
if not all(file.is_file() for file in LOG_FILES):
    map(lambda file: open(file, 'a').close(), LOG_FILES)
    # [open(file, 'a').close() for file in LOG_FILES]


# Static files (HTML, CSS, JavaScript)
STATIC_URL = ENVIRONMENT['settings']['static_url']
STATIC_ROOT = ENVIRONMENT['settings']['static_root']


# Media files (Images)
MEDIA_URL = ENVIRONMENT['settings']['media_url']
MEDIA_ROOT = ENVIRONMENT['settings']['media_root']
