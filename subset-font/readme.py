import re
from pathlib import Path
from typing import List

from .util import read_file, write_file
from .font import FontRow


class Readme:
    file: Path
    download_start = "<!-- download_start -->"
    download_end = "<!-- download_end -->"

    def __init__(self, file: Path):
        self.file = file
        if not self.file.exists():
            raise FileNotFoundError(f"{self.file} not found")

    def overwrite(self, font_rows: List[FontRow]):
        readme_content = read_file(self.file)
        rows = [
            "| 字体名称 | 文件名 | 精简前 | 精简后 | 许可证 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for row in font_rows:
            cols = [
                row.name,
                row.file_name,
                f"[下载]({row.download_link}) {row.size}",
                f"[下载]({row.subset_download_link}) {row.subset_size}",
                "暂无"
                if not row.license
                else f"[{row.license.file_name}]({row.license.link})",
            ]
            rows.append(f"| {' | '.join(cols)} |")

        linesep = "\n"
        readme_content = re.sub(
            rf"{self.download_start}.*{self.download_end}",
            lambda _: f"{self.download_start}{linesep +linesep.join(rows) +linesep}{self.download_end}",
            readme_content,
            flags=re.DOTALL,
        )

        write_file(self.file, readme_content)
