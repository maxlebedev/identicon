from PIL import Image, ImageDraw
from docopt import docopt
import colorsys
import random

golden_ratio_conjugate = 0.618033988749895


# TODO: we could cycle forward a variable number of times
def next_hue(hue: float) -> float:
    hue += golden_ratio_conjugate
    hue = hue % 1
    return hue


def hue_to_rgb(hue: float) -> tuple:
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))


def make_identicon(seed, name="simple_image"):
    random.seed(seed)

    hue = random.random()
    background_color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))

    # Create a new image with a seeded background
    width, height = 8, 8
    image = Image.new("RGB", (width, height), background_color)

    # Get a drawing object to add shapes and text
    draw = ImageDraw.Draw(image)

    hue = next_hue(hue)
    first_fg = hue_to_rgb(hue)

    hue = next_hue(hue)
    second_fg = hue_to_rgb(hue)

    # placeholder pattern
    for i in range(8):
        for j in range(16):
            cmp = random.random()
            if cmp < 0.33:
                draw.point((i, j), fill=first_fg)
                draw.point((width - i - 1, j), fill=first_fg)
            elif cmp < 0.66:
                draw.point((i, j), fill=second_fg)
                draw.point((width - i - 1, j), fill=second_fg)

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
