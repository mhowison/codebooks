from logging import DEBUG, INFO, WARN, ERROR, basicConfig, getLogger
from tqdm import tqdm

basicConfig(level=INFO)

LEVEL = 1
LOGGER = getLogger("codebooks")

def setLevel(level: int):
    global LEVEL, LOGGER
    basicConfig(level=level)
    LEVEL = level
    LOGGER = getLogger("codebooks")

def error(msg: str) -> None:
    LOGGER.error(msg)

def warn(msg: str) -> None:
    LOGGER.warn(msg)

def info(msg: str) -> None:
    LOGGER.info(msg)

def debug(msg: str ) -> None:
    LOGGER.debug(msg)

def progress(iterator):
    if LEVEL <= INFO:
        return tqdm(iterator)
    else:
        return iterator
