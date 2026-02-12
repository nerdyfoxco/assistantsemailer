import logging
import json
import datetime
from typing import Any, MutableMapping

class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings for structured logging.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: MutableMapping[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra context if provided in 'extra'
        if hasattr(record, "props"):
             log_record.update(record.props)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)

class StructuredLogger:
    """
    Wrapper around standard logging to enforce structured output.
    Phase 0: Prints to stdout via StreamHandler.
    """
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        
        # Ensure we don't add multiple handlers if re-initialized
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(JsonFormatter())
            self._logger.addHandler(handler)
            self._logger.propagate = False # Stop propagation to root logger to avoid double logs

    def info(self, msg: str, **kwargs):
        self._logger.info(msg, extra={"props": kwargs})

    def warning(self, msg: str, **kwargs):
        self._logger.warning(msg, extra={"props": kwargs})

    def error(self, msg: str, exc_info: bool = True, **kwargs):
        self._logger.error(msg, exc_info=exc_info, extra={"props": kwargs})

    @staticmethod
    def get_logger(name: str) -> 'StructuredLogger':
        return StructuredLogger(name)
