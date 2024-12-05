from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

from .font import FontRow
from .util import copy_folder, write_file


class PreviewData(BaseModel):
    fonts: List[FontRow] = Field(default_factory=list, description="List of font rows")
    subset: str = Field(default="", description="Subset text")


class Preview:
    template_folder: Path

    def __init__(self, template_folder: str):
        self.template_folder = Path(template_folder)

    def overwrite(self, dist_folder: Path, font_rows: List[FontRow], subset_text: str):
        copy_folder(self.template_folder, dist_folder)

        preview_data = PreviewData(fonts=font_rows, subset=subset_text)

        preview_data_json = preview_data.model_dump_json(
            indent=2,
            include={"fonts": {"__all__": {"name", "file_name"}}, "subset": True},
        )

        write_file(
            dist_folder / "static/data.js",
            f"window.data = {preview_data_json};",
        )
