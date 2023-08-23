from PIL import Image, ImageDraw
from docopt import docopt
import hashlib
import colorsys

golden_ratio_conjugate = 0.618033988749895


def next_hue(hue: float) -> float:
    hue += golden_ratio_conjugate
    hue = hue % 1
    return hue


def hue_to_rgb(hue: float) -> tuple:
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))


def make_identicon(seed, name="simple_image"):
    hasher = hashlib.sha1()
    hasher.update(seed.encode("utf-8"))
    seed = hasher.hexdigest()

    hue = int(seed[:2], 16) / 100
    background_color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))

    # Create a new image with a seeded background
    width, height = 16, 16
    image = Image.new("RGB", (width, height), background_color)

    # Get a drawing object to add shapes and text
    draw = ImageDraw.Draw(image)

    hue = next_hue(hue)
    first_fg = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))

    hue = next_hue(hue)
    second_fg = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))

    # placeholder pattern
    for i in range(16):
        for j in range(16):
            if i % 2 == 0 and j % 2 == 1:
                draw.point((i, j), fill=first_fg)
            if i % 2 == 1 and j % 2 == 0:
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
