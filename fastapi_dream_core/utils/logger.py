import logging

from fastapi_dream_core.environments import AppBaseEnvironments

log_level = logging.INFO

if AppBaseEnvironments().is_dev_environment():
    log_level = logging.DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

handler = logging.StreamHandler()
handler.setLevel(log_level)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
