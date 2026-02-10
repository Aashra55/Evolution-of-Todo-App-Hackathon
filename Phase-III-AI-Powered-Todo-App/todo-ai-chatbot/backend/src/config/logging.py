# backend/src/config/logging.py
import logging
import sys

def configure_logging():
    log_format = (
        '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", '
        '"name": "%(name)s", "pathname": "%(pathname)s", "lineno": %(lineno)d}'
    )
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Optionally configure loggers for specific libraries to reduce verbosity
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)