"""Configuration of loguru."""

import logging
import sys
import uuid
from contextvars import ContextVar
from pathlib import Path
from typing import Optional

from loguru import logger

from .config import settings

BASE_DIR = Path(__file__).parent
LOG_PATH = BASE_DIR / "logs" / "app.log"  # Store logs here


# ============================================
# CONTEXT VARIABLES FOR REQUEST TRACKING
# ============================================
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


# ============================================
# CUSTOM FILTER FOR CORRELATION
# ============================================


def correlation_filter(record: "Record") -> bool:
    """
    Add Request ID to log record.

    Args:
        record (Record): Log record from Loguru (contains everything about log line - message, level, time etc.)

    Returns:
        bool: True to include the log, False to filter it out.
    """

    # Get request_id. If it doesn't exist, create one. Attach to record
    record["extra"]["request_id"] = request_id_var.get() or str(uuid.uuid4())[:8]

    return True


# ============================================
# INTERCEPT HANDLER FOR STANDARD LOGGING
# ============================================


class InterceptHandler(logging.Handler):
    """
    Intercepts standard logging and redirects to Loguru.
    Used to replace Uvicorn's default loggers with our Loguru configuration.
    """

    def emit(self, record: logging.LogRecord):
        """
        Process a log record and redirect it to Loguru.

        This method is called by the logging framework for each log record. We extract the log level and message, then pass it to Loguru.
        """
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find the caller from where the logging call originated
        frame = logging.currentframe()
        depth = 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Log to Loguru with the appropriate level and context
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# ============================================
# MAIN LOGGER SETUP FUNCTION
# ============================================


def setup_logger():
    """
    Configure Loguru logger.

    This should be called once during application startup, preferably in the FastAPI lifespan startup event.
    """

    # Remove default handler to avoid duplicate logs
    logger.remove()

    # Get log level
    log_level = settings.log_level

    # Format: Timestamp | Level | RequestID | Source | Message
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<yellow>ReqID:{extra[request_id]}</yellow> | "
        "<cyan>File[{file}] Module[{name}] Function[{function}] Line[{line}]</cyan> | "
        "<level>{message}</level>"
    )

    # Console output
    logger.add(
        sys.stdout,
        format=log_format,
        level=log_level,
        colorize=True,
        enqueue=True,  # Non-blocking and safe across threads/processes
        filter=correlation_filter,
    )

    # File output
    logger.add(
        sink=LOG_PATH,
        format=log_format,
        level=log_level,
        rotation="50 MB",  # Rotate when file reaches 50MB
        retention=5,  # Rotate 5 log files
        compression="gz",  # Compress rotated files to .gz
        backtrace=True,  # Enable full traceback on exceptions
        diagnose=True,  # Show variable values in exceptions
        enqueue=True,  # Non-blocking and safe across threads/processes
        filter=correlation_filter,
    )


# ============================================
# UVICORN LOGGER CONFIGURATION
# ============================================


def configure_uvicorn_logging():
    """
    Replace Uvicorn's default logging with Loguru.

    This intercepts all standard library logging calls from Uvicorn and redirects them through our Loguru configuration, ensuring consistent log formatting across the entire application.

    Call this during FastAPI app startup, after setup_logger().
    """

    import logging

    # Intercept all loggers and set to lowest level
    # Loguru will handle the actual filtering
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Update existing loggers, especially Uvicorn loggers
    for name in logging.root.manager.loggerDict.keys():
        if name.startswith("uvicorn"):
            logging.getLogger(name).handlers = [InterceptHandler()]
            logging.getLogger(name).propagate = False

    logger.debug("Uvicorn logging configured to use Loguru.")


# ============================================
# SHUTDOWN HANDLER
# ============================================


def shutdown_logger():
    """
    Gracefully shutdown logger and flush all pending logs.

    Call this in FastAPI shutdown event.
    """

    logger.info("Shutting down logger...")

    # Let Loguru finish processing queued logs
    logger.complete()

    logger.info("Logger shutdown complete")
