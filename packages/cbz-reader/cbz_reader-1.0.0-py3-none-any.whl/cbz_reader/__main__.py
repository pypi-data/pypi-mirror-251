from base64 import b64encode
from collections import OrderedDict
import mimetypes # mimetypes.guess_type
import os # os.getcwd, os.chdir
import pathlib # pathlib.Path
import zipfile # zipfile.Path

from natsort import natsorted
import quart # quart.render_template, quart.redirect
from quart import Quart

app = Quart(__name__)
app.config.from_prefixed_env("CBZ")

CBZ_BASE_PATH = app.config.get("BASE_PATH", os.getcwd())
CBZ_BASE_PATH = pathlib.Path(CBZ_BASE_PATH)
os.chdir(CBZ_BASE_PATH)
app.logger.info(f"Looking for CBZs in: {str(CBZ_BASE_PATH.absolute())}")

CBZ = []
for file in CBZ_BASE_PATH.glob("*.cbz"):
    if not file.is_file():
        app.logger.warn(f"Ignoring: Not a file: {file.name}")
        continue

    CBZ.append(file.name)

if not CBZ:
    app.logger.fatal(f"No CBZ found in: {str(CBZ_BASE_PATH.absolute())}")
    exit(1)

CBZ = natsorted(CBZ)
app.logger.info(f"Found CBZ: {CBZ}")

CBZ_MAP = OrderedDict(enumerate(CBZ, start=1))

@app.route('/')
async def list_cbz() -> None:
    return await quart.render_template("list_cbz.html", cbz_map=CBZ_MAP.items())

@app.route('/load_cbz/<int:current_page_index>')
async def load_cbz(current_page_index: int) -> None:
    if not CBZ_MAP.get(current_page_index):
        return quart.redirect("/404")

    cbz_file_name = CBZ_MAP[current_page_index]
    app.logger.info(f"Loading in: {cbz_file_name}")
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
            app.logger.warning(f"{cbz_file.name} contains non image files: {file.name}")
            continue

        image_sources.append(file.read_bytes())
        app.logger.debug(f"Found image: {file.name}")

    image_sources = [b64encode(image_src) for image_src in image_sources]
    image_sources = [image_src.decode("utf-8") for image_src in image_sources]
    image_sources = [f"data:image/jpeg;base64,{image_src}" for image_src in image_sources]

    # CBZ_MAP is an OrderedDict
    indexes = tuple(CBZ_MAP.keys())

    # Check if current_page_index is not same as the first_page_index or the last_page_index
    first_page_index = indexes[0] if current_page_index != indexes[0] else None
    last_page_index = indexes[-1] if current_page_index != indexes[-1] else None

    previous_page_index = current_page_index - 1
    next_page_index = current_page_index + 1

    # Check if the previous_page_index and the next_page_index exist
    previous_page_index = previous_page_index if CBZ_MAP.get(previous_page_index) else None
    next_page_index = next_page_index if CBZ_MAP.get(next_page_index) else None

    return await quart.render_template(
        "load_cbz.html",
        chapter_title=chapter_title,
        image_sources=image_sources,
        current_page_index=current_page_index,
        first_page_index=first_page_index,
        last_page_index=last_page_index,
        previous_page_index=previous_page_index,
        next_page_index=next_page_index,
    )


if __name__ == "__main__":
    app.run()
