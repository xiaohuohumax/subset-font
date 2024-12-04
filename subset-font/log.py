import logging.config
from pathlib import Path

from .util import read_yaml


def configure_logging(config_file: Path):
    if config_file is None or not config_file.exists():
        return

    logging_config = read_yaml(config_file)

    for handler in logging_config.get("handlers", {}).values():
        class_name = handler.get("class", "")
        if class_name != "logging.handlers.RotatingFileHandler":
            continue
        Path(handler["filename"]).parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(config=logging_config)
