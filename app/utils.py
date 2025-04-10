import csv
import math
import pathlib
import re
from dataclasses import dataclass
from datetime import datetime, timedelta

from PIL import ExifTags, Image, ImageOps

APP_PATH = pathlib.Path.cwd() / "app"
TEMPLATES_PATH = APP_PATH / "templates"
STATIC_PATH = GALLERY_PATH = APP_PATH / "static"

GALLERY_PATH = STATIC_PATH / "gallery"
THUMBNAIL_SIZE = (640, 640)
THUMBNAIL_PATH = GALLERY_PATH / "thumbs"
THUMBNAIL_PATH.mkdir(exist_ok=True)

CUBING_PATH = STATIC_PATH / "cubing"
CUBING_FILE_REGEX = re.compile(r"Solves_333_Normal_(.+)\.txt")

# splits a duration string like "1:01.30" or "49.08" into
# groups of minutes (optional), seconds, and milliseconds.
CUBING_DURATION_REGEX = re.compile(r"(?:(\d+)(?=:):)?(\d+)\.(\d+)")


@dataclass
class TimedSolve:
    duration: timedelta
    scramble: str
    dnf: bool
    timestamp: datetime

    # define this "less than" operation such that DNF solves
    # will always be put "slower" than any others when sorting
    def __lt__(self, other):
        if other.dnf and not self.dnf:
            return True

        if self.dnf:
            return False

        return self.duration < other.duration


class CubingStats:
    def __init__(self, solves, timestamp):
        self.solves = solves
        self.timestamp = timestamp
        self._best_avg_cache = {}

    @classmethod
    def from_newest_file(cls):
        # the filename is timestamped in ISO format so we can
        # find the newest one by doing string comparisons
        newest_stats_file = max(CUBING_PATH.iterdir())

        stats_timestamp = datetime.strptime(
            CUBING_FILE_REGEX.match(newest_stats_file.name).group(1),
            r"%Y-%m-%d_%H-%M",
        )

        timed_solves = []
        with open(newest_stats_file, newline="") as csv_file:
            stats_reader = csv.reader(csv_file, delimiter=";", quotechar="\"")

            for row in stats_reader:
                # solves tagged with "DNF" have four parts rather than three
                dnf = len(row) == 4
                duration, scramble, timestamp = row[:3]

                match = CUBING_DURATION_REGEX.match(duration)
                duration = timedelta(
                    minutes=int(match.group(1) or "0"),
                    seconds=int(match.group(2)),
                    milliseconds=int(match.group(3)) * 10,
                )

                timestamp = datetime.strptime(
                    timestamp, r"%Y-%m-%dT%H:%M:%S.%f%z"
                )

                timed_solves.append(
                    TimedSolve(duration, scramble, dnf, timestamp)
                )

        # should be already sorted from the file, but just in case
        timed_solves.sort(key=lambda solve: solve.timestamp)
        return cls(timed_solves, stats_timestamp)

    def avg_of(self, sample_size, offset=0):
        if sample_size > len(self.solves):
            return None

        sample_end = len(self.solves) - offset
        sample_start = sample_end - sample_size
        sample = self.solves[sample_start:sample_end]
        sample.sort()

        # aoX is calculated after truncating the 5% extremes
        truncate = math.ceil(0.05 * sample_size)
        truncated_sample = sample[truncate:-truncate]

        # if any of the untruncated solves are DNF, then the
        # whole average becomes a DNF, represented by None.
        if truncated_sample[-1].dnf:
            return None

        total_duration = timedelta()
        for solve in truncated_sample:
            total_duration += solve.duration

        return total_duration / len(truncated_sample)

    def best_avg_of(self, sample_size):
        # this is a fairly inefficient method of calculating these
        # statistics so it's wise use a caching dictionary in order
        # to eliminate unnecessary repeated calculations
        if sample_size in self._best_avg_cache:
            return self._best_avg_cache[sample_size]

        if sample_size > len(self.solves):
            return None

        best_avg = None
        for offset in range(len(self.solves) - sample_size + 1):
            current_avg = self.avg_of(sample_size)

            if current_avg is None:
                continue

            if best_avg is None or current_avg < best_avg:
                best_avg = current_avg

        self._best_avg_cache[sample_size] = best_avg
        return best_avg


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


CUBING_STATS = CubingStats.from_newest_file()

GALLERY_IMAGES = GalleryImage.generate_gallery()

SIDEBAR_LAYOUT = SidebarGroup.generate_layout((
    ("photography", "purple"),
    ("cubing", "blue"),
    ("services", "teal"),
    ("other", "green"),
))

# we can add some links manually too
SIDEBAR_LAYOUT["services"].pages["osu!"] = "https://osu.skrungly.com/"
