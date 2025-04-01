import pathlib
from dataclasses import dataclass


# overengineered dynamic sidebar? maybe!
@dataclass
class SidebarGroup:
    title: str
    colour: str
    pages: dict[str, str]

    def __init__(self, title: str, colour: str, pages: dict):
        self.title = title
        self.colour = colour
        self.pages = pages

    @classmethod
    def generate_layout(cls, groups: tuple[str, str]):
        # for each of the provided categories, check for
        # templates in the respective directoriess to
        # generate the sidebar content procedurally
        layout = {}
        for category, colour in groups:

            # generate a relative "href" link for each template
            pages = {}
            for template in (TEMPLATES_PATH / category).iterdir():
                pages[template.stem] = f"/{category}/{template.stem}"

            layout[category] = SidebarGroup(category, colour, pages)

        return layout


TEMPLATES_PATH = pathlib.Path.cwd() / "app" / "templates"
SIDEBAR_LAYOUT = SidebarGroup.generate_layout((
    ("photography", "purple"),
    ("cubing", "blue"),
    ("services", "teal"),
    ("other", "green"),
))

# we can add some links manually too
SIDEBAR_LAYOUT["services"].pages["osu!"] = "https://osu.skrungly.com/"
