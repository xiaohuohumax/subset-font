from pathlib import Path
from typing import List

from .font import FontRow
from .util import read_file, path_url_quote, write_file, replace_comment_element


class Preview:
    file: Path
    import_fonts_styles: str = "import-fonts-styles"
    switch_button_group: str = "switch-button-group"
    subset_content: str = "subset-content"

    def __init__(self, file: str):
        self.file = Path(file)

    def overwrite(self, font_rows: List[FontRow], subset_text: str):
        preview_content = read_file(Path(__file__).parent / "preview.html")

        fonts_styles = []
        button_group = []

        for font_row in font_rows:
            file_name = font_row.file_name.split(".")[0]
            font_file_path = path_url_quote(font_row.file_name)
            fonts_styles.append(
                f"@font-face {{ font-family: \"{file_name}\"; src: url('{font_file_path}'); }}"
            )

            button_group.append(
                f'<button data-name="{file_name}">{font_row.name}</button>'
            )
        linesep = "\n"

        preview_content = replace_comment_element(
            self.import_fonts_styles,
            preview_content,
            f"<style>{linesep+ linesep.join(fonts_styles) + linesep}</style>",
        )

        preview_content = replace_comment_element(
            self.switch_button_group,
            preview_content,
            f"{linesep+ linesep.join(button_group) + linesep}",
        )

        preview_content = replace_comment_element(
            self.subset_content,
            preview_content,
            subset_text,
        )

        write_file(self.file, preview_content)
