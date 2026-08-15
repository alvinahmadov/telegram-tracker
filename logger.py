import os
import sys

from loguru import logger


def setup_logger(target_name: str | None = None, logs_dir="logs"):
    # Explicitly create the logs folder if it is not already in the project root
    os.makedirs("logs", exist_ok=True)

    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>"
    )
    
    file_name = "/".join([logs_dir or "", "{time:YYYY-MM-DD}.log"]).strip()
    
    logger.add(
        file_name,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        encoding="utf-8",
        rotation="00:00",  # Strict rotation at exactly midnight
        enqueue=True  # Useful for asynchronous code (thread safe writing)
    )
    
    return logger


custom_logger = setup_logger()
