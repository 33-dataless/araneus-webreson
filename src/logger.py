import logging
import sys
import colorlog


def configure_logging(
    level: int = logging.INFO,
    log_format: str = "~ %(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    date_format: str = "%Y-%m-%d %H:%M:%S",
) -> None:
    handler = colorlog.StreamHandler(sys.stdout)

    formatter = colorlog.ColoredFormatter(
        f"%(log_color)s{log_format}",
        datefmt=date_format,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[handler],
        force=True,
    )