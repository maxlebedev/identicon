from PIL import Image, ImageDraw
from docopt import docopt
import colorsys
import random

golden_ratio_conjugate = 0.618033988749895

def next_hue(hue: float) -> float:
    hue += golden_ratio_conjugate
    hue = hue % 1
    return hue


def hue_to_rgb(hue: float) -> tuple:
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.5, 0.95))


def draw_pattern(image: Image.Image, size: int, fg1: tuple, fg2: tuple):
    """color a quarter of the pixels one color, another quarter the other, mirror left half onto the right half"""
    draw = ImageDraw.Draw(image)

    for i in range(size // 2):
        for j in range(size):
            cmp = random.random()
            if cmp < 0.25:
                draw.point((i, j), fill=fg1)
                draw.point((size - i - 1, j), fill=fg1)
            elif cmp < 0.50:
                draw.point((i, j), fill=fg2)
                draw.point((size - i - 1, j), fill=fg2)


def generate_image(seed: str, size=8) -> Image.Image:
    random.seed(seed)

    hue = random.random()
    background_color = hue_to_rgb(hue)

    image = Image.new("RGB", (size, size), background_color)

    hue = next_hue(hue)
    first_fg = hue_to_rgb(hue)

    hue = next_hue(hue)
    second_fg = hue_to_rgb(hue)

    draw_pattern(image, size, first_fg, second_fg)
    return image


usage = """
Identicon Generator

Usage:
    identicon.py <seed> [--name=<name>]

Options:
    --name=<name>  name the output file [default: identicon]
"""
if __name__ == "__main__":
    args = docopt(usage)
    image = generate_image(args["<seed>"])
    image.save(f"{args['--name']}.png")
