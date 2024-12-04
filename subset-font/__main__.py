import logging
from typing import List

from .args import args
from .util import reade_lines, read_file
from .font import Font, FontLicense
from .readme import FontRow, Readme
from .preview import Preview

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting subset-font...")
    logger.info(f"Args: {args}")

    fonts = Font.load_fonts(args.fonts_folder, args.licenses_folder)
    logger.info(f"Loaded {len(fonts)} fonts from {args.fonts_folder}")

    subset_text = "\n".join(
        [line for line in reade_lines(args.subset_file) if not line.startswith("#")]
    )
    readme = Readme("README.md")
    preview = Preview("dist/index.html")
    download_rows: List[FontRow] = []
    success_count = 0
    fail_count = 0

    for i, font in enumerate(fonts):
        logger.info(f"{i+1}/{len(fonts)}: {font.name}({font.file})")

        try:
            subset_font = font.subset_font(subset_text, args.dist_folder)

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

    readme.overwrite(download_rows)
    preview.overwrite(download_rows, read_file(args.subset_file))

    logger.info("Done!")
    logger.info(f"Success: {success_count}, Fail: {fail_count}")
