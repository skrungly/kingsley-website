import pathlib

from flask import abort, render_template

from app import app
from app.utils import (
    CUBING_STATS,
    GALLERY_IMAGES,
    NAVBAR_LAYOUT,
    TEMPLATES_PATH,
)


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="home",
        content_colour="red",
        navbar=NAVBAR_LAYOUT,
    )


@app.route("/<path:subpath>")
def category_page(subpath: str):
    template = pathlib.Path(subpath).with_suffix(".html")
    if not (TEMPLATES_PATH / template).exists():
        abort(404)

    # split the route path to get category info.
    # if a page is missing from the navbar (e.g. it got auto-removed for
    # lack of content, like a gallery without images) then return a 404.
    category, page = pathlib.Path(subpath).parts[:2]
    if category not in NAVBAR_LAYOUT or page not in NAVBAR_LAYOUT[category].pages:
        abort(404)

    return render_template(
        str(template),
        title=page,
        content_colour=NAVBAR_LAYOUT[category].colour,
        navbar=NAVBAR_LAYOUT,
        gallery_images=GALLERY_IMAGES,
        cubing_stats=CUBING_STATS,
    )
