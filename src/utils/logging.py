from loguru import logger
import sys


def setup_logging(log_level: str = "INFO") -> None:
    # INFO and above
    logger.remove()         # remove default handler
    logger.add(             # send a log to the terminal
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}",
        level=log_level,
        colorize=True,
    )                       # every log go to pipeline so i can read it later
    logger.add(
        "logs/pipeline.log",
        rotation="10 MB",
        level="DEBUG",
    )
