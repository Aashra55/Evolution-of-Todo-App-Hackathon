import logging
import json
import os
from datetime import datetime

# Define a custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": os.environ.get("DAPR_APP_ID", "unknown-service"), # Use DAPR_APP_ID if available
            "logger": record.name,
            "file": f"{record.filename}:{record.lineno}",
            "func": record.funcName,
            "traceId": os.environ.get("DAPR_TRACE_ID", None), # Dapr trace ID
            "spanId": os.environ.get("DAPR_SPAN_ID", None),   # Dapr span ID
            "correlationId": getattr(record, 'correlationId', None) # Custom correlation ID
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        # Add any extra attributes attached to the record
        for key, value in record.__dict__.items():
            if key not in ["name", "msg", "levelname", "pathname", "filename", 
                           "lineno", "funcName", "created", "msecs", "relativeCreated",
                           "thread", "threadName", "processName", "process", 
                           "exc_info", "exc_text", "stack_info", "args", "kwargs",
                           "asctime", "module", "levelno", "rpcId", "traceId", "spanId", "correlationId"]:
                log_record[key] = value

        return json.dumps(log_record)

def setup_logging():
    # Clear existing handlers to prevent duplicate logs in some environments
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    handler = logging.StreamHandler()
    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[handler])

    # Optionally, set Dapr's Python SDK logger to WARNING or ERROR to reduce verbosity
    logging.getLogger('dapr.clients').setLevel(logging.WARNING)
    logging.getLogger('dapr.runtime').setLevel(logging.WARNING)
