from pathlib import Path

from loguru import logger

BASE_DIR = Path(__file__).parent
LOG_PATH = BASE_DIR / "logs" / "app.log"

logger.remove()

logger.add(
    sink=LOG_PATH,
    rotation="10 MB",
    retention=5,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file} | Line: {line} | {message}"
)
