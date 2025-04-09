import pathlib
from dataclasses import dataclass

from PIL import ExifTags, Image, ImageOps


APP_PATH = pathlib.Path.cwd() / "app"
TEMPLATES_PATH = APP_PATH / "templates"
STATIC_PATH = GALLERY_PATH = APP_PATH / "static"
GALLERY_PATH = STATIC_PATH / "gallery"
CUBING_PATH = STATIC_PATH / "assets" / "cubing"

THUMBNAIL_SIZE = (640, 640)
THUMBNAIL_PATH = GALLERY_PATH / "thumbs"
THUMBNAIL_PATH.mkdir(exist_ok=True)

CUBING_FILE_REGEX = re.compile("Solves_333_Normal_(.*).txt")


class GalleryImage:
    def __init__(self, img_path):
        with Image.open(img_path) as img:
            ImageOps.exif_transpose(img, in_place=True)

            thumb = THUMBNAIL_PATH / img_path.name
            if not thumb.exists():
                img.thumbnail(THUMBNAIL_SIZE)
                img.save(thumb)

        self.path = img_path.relative_to(STATIC_PATH)
        self.thumb = thumb.relative_to(STATIC_PATH)
        self.metadata = self._format_exif(img, img_path)

    @staticmethod
    def _format_exif(img, img_path):
        metadata_lines = [img_path.name]

        # bit of a hack, but it works
        if img_path.name.startswith("HNI_"):
            metadata_lines.append("Nintendo DSi")
            metadata_lines.append("640x480 (0.3MP)")

        exif = img._getexif()
        if not exif:
            return "\n".join(metadata_lines)

        exif_tags = {ExifTags.TAGS.get(k, k): v for k, v in exif.items()}

        photo_spec = []
        if exp_time := exif_tags.get("ExposureTime"):
            photo_spec.append(
                f"1/{1 / exp_time:.0f}\"" if exp_time < 1 else f"{exp_time}\""
            )

        if f_stop := exif_tags.get("FNumber"):
            photo_spec.append(f"f/{float(f_stop):.2g}")

        if focal_length := exif_tags.get("FocalLength"):
            photo_spec.append(f"{float(focal_length):.0f}mm")

        if iso_speed := exif_tags.get("ISOSpeedRatings"):
            photo_spec.append(f"ISO{iso_speed}")

        megapixels = (img.width * img.height) / 1000000
        photo_spec.append(f"{img.width}x{img.height} ({megapixels:.01f}MP)")

        metadata_lines.append(exif_tags["Model"] or "Unknown camera")
        metadata_lines.append(" ".join(photo_spec))

        if caption := exif_tags.get("ImageDescription"):
            metadata_lines.append("\n" + caption)

        return "\n".join(metadata_lines)

    @classmethod
    def generate_gallery(cls):
        print(" * Ensuring gallery thumbnails are present...")

        img_paths = []
        for file in GALLERY_PATH.iterdir():
            if file.is_file():
                img_paths.append(file)

        gallery = []
        padding = len(str(len(img_paths)))
        for i, file in enumerate(img_paths, 1):
            print(f"     ({i:0{padding}d}/{len(img_paths)}) {file.name}")
            gallery.append(cls(file))

        return gallery


GALLERY_IMAGES = GalleryImage.generate_gallery()


# overengineered dynamic sidebar? maybe!
@dataclass
class SidebarGroup:
    title: str
    colour: str
    pages: dict[str, str]

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


SIDEBAR_LAYOUT = SidebarGroup.generate_layout((
    ("photography", "purple"),
    ("cubing", "blue"),
    ("services", "teal"),
    ("other", "green"),
))

# we can add some links manually too
SIDEBAR_LAYOUT["services"].pages["osu!"] = "https://osu.skrungly.com/"
