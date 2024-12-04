from pathlib import Path

from .log import configure_logging
from .util import read_file

configure_logging(Path("logging.yaml"))


def banner(file: Path):
    if not file.exists():
        return
    print(read_file(file))


banner(Path("banner.txt"))
