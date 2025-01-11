import logging
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import List, Optional, Tuple

from .args import args
from .font import Font, FontLicense
from .preview import Preview
from .readme import FontRow, Readme
from .util import clear_folder, read_file, read_file_without_comments

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting subset-font...")
    logger.info(f"Args: {args}")

    fonts = Font.load_fonts(args.fonts_folder, args.licenses_folder)
    logger.info(f"Loaded {len(fonts)} fonts from {args.fonts_folder}")

    subset_text = read_file(args.subset_file)
    subset_text_without_comments = read_file_without_comments(args.subset_file)

    clear_folder(args.dist_folder)

    def subset_font_job(font: Font) -> Tuple[bool, Optional[FontRow]]:
        try:
            subset_font = font.subset_font(
                subset_text_without_comments, args.dist_folder
            )

            license = None
            if font.license_file.exists():
                license = FontLicense(
                    file_name=font.license_file.name,
                    link=font.license_link,
                )

            font_row = FontRow(
                name=font.name,
                file_name=font.file.name,
                size=font.size,
                subset_size=subset_font.size,
                download_link=font.download_link,
                subset_download_link=subset_font.download_link,
                license=license,
            )

            logger.info(
                f"Subset success [{font.name}] {font.size} => {subset_font.size}"
            )
            return (True, font_row)
        except Exception as e:
            logger.error(f"Subset failed [{font.name}]: {e}")
            return (False, None)

    pool = ThreadPool(args.thread_max)
    results = []

    for i, font in enumerate(fonts):
        logger.info(f"{i + 1}/{len(fonts)}: {font.name}({font.file})")
        results.append(pool.apply_async(subset_font_job, args=(font,)))

    pool.close()
    pool.join()

    font_rows: List[FontRow] = []
    success_count = 0
    fail_count = 0

    for result in results:
        success, font_row = result.get()
        if success:
            success_count += 1
            font_rows.append(font_row)
        else:
            fail_count += 1

    Readme(Path("README.md")).overwrite(font_rows)
    Preview(Path(__file__).parent / "preview").overwrite(
        args.dist_folder, font_rows, subset_text
    )

    logger.info(f"Success: {success_count}, Fail: {fail_count}")
    logger.info("Done!")
