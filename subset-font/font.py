from pathlib import Path
from urllib.parse import urljoin
from typing import List, Optional

from fontTools import subset
from pydantic import BaseModel, computed_field, Field

from .util import get_file_size, path_url_quote


class Font(BaseModel):
    file: Path = Field(description="Font file path")
    licenses_folder: Path = Field(description="Folder path to store font licenses")
    name: str = Field(default="", description="Font name")
    size: str = Field(default="", description="Font size")
    license_file: Path = Field(default=Path(""), description="Font license file path")
    font_family: str = Field(default="", description="Font family")
    version: str = Field(default="", description="Font version")
    copyright: str = Field(default="", description="Font copyright")

    def __init__(self, file: Path, licenses_folder: Path):
        super().__init__(file=file, licenses_folder=licenses_folder)

        names = []
        with subset.load_font(self.file, subset.Options()) as font:
            records = font["name"].names

            names.extend(
                [
                    record.toUnicode()
                    for record in records
                    if record.nameID == 4 and record.langID in [0x0404, 0x0804]
                ]
            )
            names.extend(
                [record.toUnicode() for record in records if record.nameID == 1]
            )
            names.append(self.file.stem)

            for record in records:
                record_value = record.toUnicode()
                if record.nameID == 1:
                    self.font_family = record_value
                elif record.nameID == 5:
                    self.version = record_value
                elif record.nameID == 0:
                    self.copyright = record_value

        self.name = names[0]
        self.size = get_file_size(self.file)
        self.license_file = self.licenses_folder / (self.file.stem + ".txt")

    @classmethod
    def is_font(cls, file: Path) -> bool:
        return file.suffix in [".ttf", ".otf", ".woff", ".woff2"]

    @classmethod
    def load_fonts(cls, folder: Path, licenses_folder: Path) -> List["Font"]:
        return [
            Font(font, licenses_folder)
            for font in folder.iterdir()
            if Font.is_font(font)
        ]

    @computed_field
    @property
    def download_link(self) -> str:
        return urljoin(
            "https://github.com/xiaohuohumax/subset-font/raw/main/",
            path_url_quote(self.file),
        )

    @computed_field
    @property
    def license_link(self) -> str:
        return path_url_quote(self.license_file)

    def subset_font(self, subset_text: str, dist_folder: Path) -> "Font":
        dist_font_file = dist_folder / self.file.name
        dist_font_file.parent.mkdir(parents=True, exist_ok=True)

        with subset.load_font(self.file, subset.Options()) as font:
            sub = subset.Subsetter()
            sub.populate(text=subset_text)
            sub.subset(font)
            font.save(dist_font_file)

        output_font = Font(dist_font_file, self.licenses_folder)
        return output_font


class FontLicense(BaseModel):
    file_name: str = Field(..., title="License file Name")
    link: str = Field(..., title="License Link")


class FontRow(BaseModel):
    name: str = Field(..., title="Font Name")
    file_name: str = Field(..., title="Font file Name")
    size: str = Field(..., title="Font size")
    subset_size: str = Field(..., title="Subset size")
    download_link: str = Field(..., title="Download Link")
    subset_download_link: str = Field(..., title="Subset Download Link")
    license: Optional[FontLicense] = Field(..., title="License")


if __name__ == "__main__":
    font_file = Path("./fonts/ChillRoundGothic_Regular.otf")
    print(Font.is_font(font_file))
    print(Font(file=font_file))
