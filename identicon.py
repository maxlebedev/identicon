from PIL import Image, ImageDraw
from docopt import docopt
import hashlib
import colorsys

golden_ratio_conjugate = 0.618033988749895


# TODO: we could cycle forward a variable number of times
def next_hue(hue: float) -> float:
    hue += golden_ratio_conjugate
    hue = hue % 1
    return hue


def hue_to_rgb(hue: float) -> tuple:
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))


def next_seq_chunk(inp):
    """A generator to divide a sequence into chunks units."""

    seq = None
    while True:
        if not seq:
            seq = inp
        yield int(seq[:2], 16) / 255
        seq = seq[2:]


def make_identicon(seed, name="simple_image"):
    hasher = hashlib.sha1()
    hasher.update(seed.encode("utf-8"))
    seed = hasher.hexdigest()

    seq = next_seq_chunk(seed)

    hue = next(seq)
    background_color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))

    # Create a new image with a seeded background
    width, height = 16, 16
    image = Image.new("RGB", (width, height), background_color)

    # Get a drawing object to add shapes and text
    draw = ImageDraw.Draw(image)

    hue = next_hue(hue)
    first_fg = hue_to_rgb(hue)

    hue = next_hue(hue)
    second_fg = hue_to_rgb(hue)

    # placeholder pattern
    for i in range(16):
        for j in range(16):
            cmp = next(seq)
            if cmp < 0.33:
                draw.point((i, j), fill=first_fg)
            elif cmp < 0.66:
                draw.point((i, j), fill=second_fg)

    image.save(f"{name}.png")


usage = """
Identicon Generator

Usage:
    identicon.py <seed> [--name=<name>]

Options:
    --name=<name>  name the output file [default: "simple_image"]
"""
# TODO: allow for image name arg
if __name__ == "__main__":
    args = docopt(usage)
    make_identicon(args["<seed>"])
