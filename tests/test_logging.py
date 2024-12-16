from terminal_app.logging import register_logger
from logging import Logger
from pathlib import Path



logger = register_logger("test.log")

logger.info("A")
logger.error("B")
