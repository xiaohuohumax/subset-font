import logging
from typing import List
from pathlib import Path

from .args import args
from .util import reade_lines, read_file, clear_folder
from .font import Font, FontLicense
from .readme import FontRow, Readme
from .preview import Preview

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting subset-font...")
    logger.info(f"Args: {args}")

    fonts = Font.load_fonts(args.fonts_folder, args.licenses_folder)
    logger.info(f"Loaded {len(fonts)} fonts from {args.fonts_folder}")

    subset_text = read_file(args.subset_file)
    subset_format_text = "\n".join(
        [line for line in reade_lines(args.subset_file) if not line.startswith("#")]
    )

    download_rows: List[FontRow] = []
    success_count = 0
    fail_count = 0

    clear_folder(args.dist_folder)

    for i, font in enumerate(fonts):
        logger.info(f"{i+1}/{len(fonts)}: {font.name}({font.file})")

        try:
            subset_font = font.subset_font(subset_format_text, args.dist_folder)

            license = None
            if font.license_file.exists():
                license = FontLicense(
                    file_name=font.license_file.name,
                    link=font.license_link,
                )

            download_rows.append(
                FontRow(
                    name=font.name,
                    file_name=font.file.name,
                    size=font.size,
                    subset_size=subset_font.size,
                    download_link=font.download_link,
                    subset_download_link=subset_font.download_link,
                    license=license,
                )
            )

            logger.info(f"Subset success {font.size} => {subset_font.size}")
            success_count += 1
        except Exception as e:
            logger.error(f"Subset failed: {e}")
            fail_count += 1

    Readme(Path("README.md")).overwrite(download_rows)
    Preview(Path(__file__).parent / "preview").overwrite(
        args.dist_folder, download_rows, subset_text
    )

    logger.info("Done!")
    logger.info(f"Success: {success_count}, Fail: {fail_count}")
