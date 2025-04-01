import pathlib

from flask import abort, render_template

from app import app
from app.constants import TEMPLATES_PATH, SIDEBAR_LAYOUT


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="home",
        content_colour="red",
        sidebar=SIDEBAR_LAYOUT,
    )


@app.route("/<path:subpath>")
def category_page(subpath: str):
    template = pathlib.Path(subpath).with_suffix(".html")
    if not (TEMPLATES_PATH / template).exists():
        abort(404)

    # split the route path to get category info
    category, page = pathlib.Path(subpath).parts[:2]
    return render_template(
        str(template),
        title=page,
        content_colour=SIDEBAR_LAYOUT[category].colour,
        sidebar=SIDEBAR_LAYOUT,
    )
