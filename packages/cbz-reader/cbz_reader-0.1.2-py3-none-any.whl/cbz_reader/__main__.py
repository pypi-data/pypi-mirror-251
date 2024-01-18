import logging # logging.info, logging.warning, logging.debug
from base64 import b64encode
import mimetypes # mimetypes.guess_type
import os # os.getcwd, os.chdir
import pathlib # pathlib.Path
import zipfile # zipfile.Path

import quart # quart.render_template, quart.redirect
from quart import Quart

app = Quart(__name__)
app.config.from_prefixed_env("CBZ")

CBZ_BASE_PATH = app.config.get("BASE_PATH", os.getcwd())
CBZ_BASE_PATH = pathlib.Path(CBZ_BASE_PATH)
os.chdir(CBZ_BASE_PATH)
logging.info(f"Looking for CBZs in: {str(CBZ_BASE_PATH.absolute())}")

CBZ = []
for file in CBZ_BASE_PATH.glob("*.cbz"):
    if not file.is_file():
        logging.warn(f"Ignoring: Not a file: {file.name}")
        continue

    CBZ.append(file.name)

if not CBZ:
    logging.fatal(f"No CBZ found in: {str(CBZ_BASE_PATH.absolute())}")
    exit(1)

logging.info(f"Found CBZ: {CBZ}")

@app.route('/')
async def list_cbz() -> None:
    return await quart.render_template("list_cbz.html", list_cbz=CBZ)

@app.route('/load_cbz/<cbz_file_name>')
async def load_cbz(cbz_file_name: str) -> None:
    if not cbz_file_name in CBZ:
        return quart.redirect("/404")

    logging.info(f"Loading in: {cbz_file_name}")
    cbz_file = CBZ_BASE_PATH.joinpath(cbz_file_name)
    cbz_file = zipfile.Path(cbz_file)

    chapter_title = cbz_file.stem

    image_sources = []
    for file in cbz_file.iterdir():
        if file.is_dir():
            raise ValueError(f"{cbz_file.name} contains dirs: {file.name}")

        file_type = mimetypes.guess_type(file.name)
        file_type = file_type[0]
        if file_type:
            file_type = file_type.split("/")[0] # pick image from image/aces
        if file_type != "image":
            logging.warning(f"{cbz_file.name} contains non image files: {file.name}")
            continue

        image_sources.append(file.read_bytes())
        logging.debug(f"Found image: {file.name}")

    image_sources = [b64encode(image_src) for image_src in image_sources]
    image_sources = [image_src.decode("utf-8") for image_src in image_sources]
    image_sources = [f"data:image/jpeg;base64,{image_src}" for image_src in image_sources]

    if cbz_file_name in CBZ:
        current_page_index = CBZ.index(cbz_file_name)
        previous_page_index = current_page_index - 1
        next_page_index = current_page_index + 1

        previous_page = CBZ[previous_page_index] if previous_page_index > 0 and previous_page_index < len(CBZ) else None
        next_page = CBZ[next_page_index] if next_page_index > 0 and next_page_index < len(CBZ) else None
    else:
        current_page_index = None
        current_page = None
        previous_page = None
        next_page = None

    first_page = CBZ[0] if current_page_index != 0 else None
    last_page = CBZ[-1] if current_page_index != len(CBZ) - 1 else None

    return await quart.render_template(
        "load_cbz.html",
        chapter_title=chapter_title,
        image_sources=image_sources,
        current_page_index=current_page_index,
        previous_page=previous_page,
        next_page=next_page,
        first_page=first_page,
        last_page=last_page,
    )


if __name__ == "__main__":
    app.run()
