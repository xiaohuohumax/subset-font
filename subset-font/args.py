import argparse
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


def file_exists(file_path):
    if not Path(file_path).exists():
        raise argparse.ArgumentTypeError(f"{file_path} does not exist")
    return file_path


class Args(BaseModel):
    fonts_folder: Optional[Path] = Field(
        default_factory=lambda: Path("fonts"),
        description="Fonts folder",
    )
    dist_folder: Optional[Path] = Field(
        default_factory=lambda: Path("dist"),
        description="subset fonts dist folder",
    )
    licenses_folder: Optional[Path] = Field(
        default_factory=lambda: Path("licenses"),
        description="Licenses folder",
    )
    subset_file: Optional[Path] = Field(
        default_factory=lambda: Path("subset.txt"),
        description="Subset file path",
    )
    thread_max: Optional[int] = Field(
        default=10,
        description="Max thread count",
    )


parser = argparse.ArgumentParser(
    prog="python -m subset-font",
    add_help=False,
    description="Welcome to subset-font util",
)
parser.add_argument(
    "-h",
    "--help",
    action="help",
    help="Show this help message and exit",
)
parser.add_argument(
    "-f",
    "--fonts-folder",
    dest="fonts_folder",
    type=file_exists,
    default=Path("fonts"),
    help="Fonts folder",
)
parser.add_argument(
    "-d",
    "--dist-folder",
    dest="dist_folder",
    type=str,
    default=Path("dist"),
    help="subset fonts dist folder",
)
parser.add_argument(
    "-l",
    "--licenses-folder",
    dest="licenses_folder",
    type=file_exists,
    default=Path("licenses"),
    help="Licenses folder",
)
parser.add_argument(
    "-s",
    "--subset-file",
    dest="subset_file",
    type=file_exists,
    default=Path("subset.txt"),
    help="Subset file path",
)


def min_integer(min_value):
    def check(value):
        v = int(value)
        if v < min_value:
            raise argparse.ArgumentTypeError(
                f"{value} is an invalid int value, must be at least {min_value}"
            )
        return v

    return check


parser.add_argument(
    "-t",
    "--thread-max",
    dest="thread_max",
    type=min_integer(1),
    default=10,
    help="Max thread count",
)

args = Args.model_validate(vars(parser.parse_args()))
