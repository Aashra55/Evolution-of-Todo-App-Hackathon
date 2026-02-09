import logging
import os
import json
from typing import Dict, Any

def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Custom JSON formatter
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record: Dict[str, Any] = {
                "timestamp": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "name": record.name,
                "message": record.getMessage(),
            }
            if record.exc_info:
                log_record["exc_info"] = self.formatException(record.exc_info)
            if record.stack_info:
                log_record["stack_info"] = self.formatStack(record.stack_info)
            
            # Add extra attributes if present
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
                               'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
                               'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
                               'processName', 'process', 'taskName', 'message'] and not key.startswith('_'):
                    log_record[key] = value

            return json.dumps(log_record)

    handler = logging.StreamHandler()
    formatter = JsonFormatter('%Y-%m-%dT%H:%M:%S%z')
    handler.setFormatter(formatter)

    # Get root logger and set level
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicate logs
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)
    
    root_logger.addHandler(handler)

    # Suppress verbose loggers if not in DEBUG mode
    if log_level != "DEBUG":
        logging.getLogger("httpx").setLevel(logging.WARNING) # For ToolHandler
