import re
from pathlib import Path
from typing import Any, List
from urllib.parse import quote


def read_file(file: Path, encoding="utf-8") -> str:
    with open(file, "r", encoding=encoding) as f:
        return f.read()


def write_file(file: Path, content: str, encoding="utf-8") -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w", encoding=encoding) as f:
        f.write(content)


def reade_lines(file: Path, encoding="utf-8") -> List[str]:
    return read_file(file, encoding).splitlines()


def read_yaml(file: Path, encoding="utf-8") -> Any:
    from ruamel.yaml import YAML

    file_content = read_file(file, encoding)
    return YAML(typ="safe").load(file_content)


def get_file_size(file: Path) -> str:
    size = file.stat().st_size
    if size < 1024:
        return f"{size}B"
    elif size < 1024**2:
        return f"{size / 1024:.2f}KB"
    elif size < 1024**3:
        return f"{size / 1024 ** 2:.2f}MB"
    else:
        return f"{size / 1024 ** 3:.2f}GB"


def path_url_quote(path: Path) -> str:
    return quote(str(path).replace("\\", "/"))


def replace_comment_element(comment: str, data: str, replace_data: str) -> str:
    return re.sub(
        rf"<!-- {comment} -->",
        lambda _: replace_data,
        data,
        flags=re.DOTALL,
    )
