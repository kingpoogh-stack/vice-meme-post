#!/usr/bin/env python3
"""
Draw the gta6-meme-x-01 meme with Pillow.

The picture is a flat illustration on a 1200 by 1200 canvas:
a Leonida beach at sunset, a bench in the lower half, an exhausted
gamer holding a GTA VI case on the left side of the bench, and the
make.fun ghost sitting on the right side of the bench with sunglasses,
a fan of cash and a laptop that shows a trophy.

Everything is drawn from simple shapes so the image stays sharp and
readable when it is shrunk to 480 by 480. The script is deterministic:
no randomness, no clock, no external files apart from the font.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_SIZE = 1200
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTPUT_PATH = "meme.png"


def load_font(size):
    """Return the bold font at the requested size."""
    return ImageFont.truetype(FONT_PATH, size)


def draw_sunset_sky(draw, width, height):
    """Paint a vertical sunset gradient from deep purple to orange."""
    top_colour = (52, 24, 92)
    middle_colour = (166, 62, 118)
    bottom_colour = (255, 133, 51)
    horizon = 820
    for y in range(horizon):
        ratio = y / horizon
        if ratio < 0.55:
            local = ratio / 0.55
            red = int(top_colour[0] + (middle_colour[0] - top_colour[0]) * local)
            green = int(top_colour[1] + (middle_colour[1] - top_colour[1]) * local)
            blue = int(top_colour[2] + (middle_colour[2] - top_colour[2]) * local)
        else:
            local = (ratio - 0.55) / 0.45
            red = int(middle_colour[0] + (bottom_colour[0] - middle_colour[0]) * local)
            green = int(middle_colour[1] + (bottom_colour[1] - middle_colour[1]) * local)
            blue = int(middle_colour[2] + (bottom_colour[2] - middle_colour[2]) * local)
        draw.line([(0, y), (width, y)], fill=(red, green, blue))


def draw_sun(draw):
    """Draw a big low sun sitting just above the horizon."""
    draw.ellipse([460, 470, 740, 750], fill=(255, 204, 92))
    draw.ellipse([485, 495, 715, 725], fill=(255, 219, 120))


def draw_skyline(draw):
    """Draw simple dark skyline silhouettes along the horizon."""
    silhouette = (38, 22, 62)
    buildings = [
        (40, 650, 130, 820),
        (145, 610, 230, 820),
        (880, 620, 965, 820),
        (975, 660, 1060, 820),
        (1070, 600, 1160, 820),
    ]
    for left, top, right, bottom in buildings:
        draw.rectangle([left, top, right, bottom], fill=silhouette)
    # A few lit windows, kept tiny and regular.
    window_colour = (255, 214, 110)
    for x in (165, 195, 900, 930, 1095, 1125):
        for y in (650, 700, 750):
            draw.rectangle([x, y, x + 10, y + 14], fill=window_colour)


def draw_beach(draw, width):
    """Draw the sand strip at the bottom of the picture."""
    draw.rectangle([0, 820, width, 1200], fill=(238, 203, 144))
    draw.rectangle([0, 820, width, 842], fill=(255, 226, 168))
    # A thin water line where the sea meets the sand.
    draw.rectangle([0, 800, width, 822], fill=(44, 168, 178))


def draw_palm_tree(draw, base_x, base_y, lean):
    """Draw one palm tree with a curved trunk and flat fronds."""
    trunk_colour = (92, 58, 38)
    leaf_colour = (28, 138, 84)
    top_x = base_x + lean
    top_y = base_y - 250
    # Trunk made from stacked thick line segments.
    steps = 10
    for step in range(steps):
        t0 = step / steps
        t1 = (step + 1) / steps
        x0 = base_x + lean * (t0 * t0)
        y0 = base_y - 250 * t0
        x1 = base_x + lean * (t1 * t1)
        y1 = base_y - 250 * t1
        draw.line([(x0, y0), (x1, y1)], fill=trunk_colour, width=22)
    # Fronds as thick arcs fanning out from the crown.
    for offset in (-95, -60, -25, 10, 45, 80):
        end_x = top_x + offset * 1.7
        end_y = top_y + 42 + abs(offset) // 3
        draw.line([(top_x, top_y), (top_x + offset, top_y - 38), (end_x, end_y)],
                  fill=leaf_colour, width=13, joint="curve")
    # Two coconuts under the crown.
    draw.ellipse([top_x - 18, top_y + 2, top_x + 4, top_y + 24], fill=(110, 74, 42))
    draw.ellipse([top_x + 4, top_y + 6, top_x + 26, top_y + 28], fill=(110, 74, 42))


def draw_bench(draw):
    """Draw a simple wooden bench across the lower half."""
    wood = (146, 92, 52)
    wood_dark = (110, 66, 36)
    # Backrest slats.
    draw.rectangle([270, 830, 930, 862], fill=wood)
    draw.rectangle([270, 876, 930, 908], fill=wood)
    # Seat slat.
    draw.rectangle([250, 950, 950, 986], fill=wood_dark)
    # Supports and legs.
    draw.rectangle([292, 862, 316, 986], fill=(52, 42, 52))
    draw.rectangle([884, 862, 908, 986], fill=(52, 42, 52))
    draw.rectangle([292, 986, 316, 1062], fill=(52, 42, 52))
    draw.rectangle([884, 986, 908, 1062], fill=(52, 42, 52))
    draw.rectangle([250, 1048, 950, 1066], fill=(52, 42, 52))


def draw_outlined_text(draw, centre_x, y, text, font, fill=(255, 255, 255)):
    """Draw one centred line of bold text with a thick black outline."""
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=6)
    text_width = bbox[2] - bbox[0]
    x = centre_x - text_width // 2
    draw.text((x, y), text, font=font, fill=fill,
              stroke_width=6, stroke_fill=(0, 0, 0))
    return y + (bbox[3] - bbox[1])


def draw_caption(draw, width):
    """Draw the top and bottom captions in the meme lettering style."""
    top_font = load_font(72)
    bottom_font = load_font(62)
    draw_outlined_text(draw, width // 2, 36, "WAITED 13 YEARS", top_font)
    draw_outlined_text(draw, width // 2, 122, "FOR GTA 6", top_font)
    draw_outlined_text(draw, width // 2, 1032, "MY AI AGENT JUST WON", bottom_font)
    draw_outlined_text(draw, width // 2, 1110, "BOUNTIES ON make.fun", bottom_font)


def draw_gamer(draw):
    """Draw the exhausted gamer sitting on the left side of the bench."""
    skin = (242, 184, 138)
    hoodie = (52, 92, 168)
    hoodie_dark = (38, 68, 128)
    trousers = (44, 44, 58)
    # Legs stretched out in front of the bench seat.
    draw.rectangle([352, 958, 468, 992], fill=trousers)
    draw.rectangle([352, 992, 388, 1050], fill=trousers)
    # Sneakers.
    draw.ellipse([330, 1038, 398, 1068], fill=(245, 245, 245))
    draw.rectangle([330, 1056, 398, 1068], fill=(210, 60, 60))
    # Torso in a hoodie, slumped a little.
    draw.rounded_rectangle([368, 800, 492, 970], radius=28, fill=hoodie)
    draw.rectangle([368, 930, 492, 970], fill=hoodie_dark)
    # Head, tired face.
    draw.ellipse([388, 692, 488, 792], fill=skin)
    # Half closed eyes and a flat tired mouth.
    draw.line([(408, 742), (430, 742)], fill=(30, 30, 30), width=5)
    draw.line([(448, 742), (470, 742)], fill=(30, 30, 30), width=5)
    draw.line([(420, 772), (458, 772)], fill=(30, 30, 30), width=4)
    # Cap worn backwards-ish, brim to the front.
    draw.pieslice([384, 672, 492, 762], start=180, end=360, fill=(214, 52, 64))
    draw.rectangle([478, 706, 522, 722], fill=(214, 52, 64))
    # Arm reaching down to hold the game case.
    draw.line([(478, 850), (528, 908)], fill=hoodie, width=30)
    draw.ellipse([516, 896, 544, 924], fill=skin)
    # Plain game case with hand lettered style text on it.
    draw.rectangle([520, 852, 606, 952], fill=(24, 24, 32), outline=(255, 255, 255), width=4)
    case_font = load_font(28)
    draw.text((534, 876), "GTA", font=case_font, fill=(255, 255, 255))
    draw.text((540, 908), "VI", font=case_font, fill=(255, 205, 80))


def draw_makefun_ghost(draw):
    """Draw the make.fun ghost sitting on the right side of the bench."""
    ghost_fill = (255, 255, 255)
    ghost_outline = (30, 30, 40)
    left, top, right = 650, 668, 842
    bottom = 972
    # Body: a rounded dome on top of a straight sided shape.
    draw.pieslice([left, top, right, top + 192], start=180, end=360, fill=ghost_fill)
    draw.rectangle([left, top + 96, right, bottom - 26], fill=ghost_fill)
    # Wavy bottom edge made from overlapping circles.
    wave_y = bottom - 26
    for index in range(4):
        cx = left + 24 + index * 48
        draw.ellipse([cx, wave_y, cx + 48, wave_y + 48], fill=ghost_fill)
    # Clean outline hints on the sides.
    draw.line([(left, top + 96), (left, bottom - 8)], fill=ghost_outline, width=3)
    draw.line([(right, top + 96), (right, bottom - 8)], fill=ghost_outline, width=3)
    draw.arc([left, top, right, top + 192], start=180, end=360, fill=ghost_outline, width=3)
    # Friendly eyes behind sunglasses.
    draw.rounded_rectangle([678, 742, 814, 786], radius=18, fill=(18, 18, 22))
    draw.rectangle([678, 754, 814, 762], fill=(60, 60, 70))
    draw.line([(650, 750), (678, 758)], fill=(18, 18, 22), width=7)
    draw.line([(814, 758), (842, 750)], fill=(18, 18, 22), width=7)
    # Smile under the glasses.
    draw.arc([706, 782, 786, 836], start=15, end=165, fill=ghost_outline, width=5)
    # Name written on the belly, kept clear of the cash hand.
    belly_font = load_font(30)
    bbox = draw.textbbox((0, 0), "make.fun", font=belly_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((left + right - text_width) // 2 - 14, 834), "make.fun",
              font=belly_font, fill=(198, 32, 120))
    # One arm holding a fan of green cash out to the side.
    cash_green = (38, 168, 92)
    cash_dark = (24, 128, 68)
    for angle_offset in (-52, -26, 0, 26):
        x0 = 844 + angle_offset
        draw.polygon([(838, 880), (x0 + 66, 800), (x0 + 96, 820), (862, 904)],
                     fill=cash_green, outline=cash_dark)
    draw.ellipse([828, 870, 864, 906], fill=ghost_fill, outline=ghost_outline, width=3)
    # Small laptop on the lap showing a tiny trophy.
    draw.rectangle([676, 908, 800, 972], fill=(38, 38, 48))
    draw.rectangle([686, 918, 790, 962], fill=(92, 190, 230))
    # Trophy: cup, stem and base in gold.
    draw.polygon([(720, 926), (756, 926), (750, 946), (726, 946)], fill=(255, 196, 0))
    draw.rectangle([734, 946, 742, 954], fill=(255, 196, 0))
    draw.rectangle([726, 954, 750, 960], fill=(230, 168, 0))


def draw_speech_bubble(draw):
    """Draw the ghost's speech bubble with its short punchline."""
    bubble_box = [742, 548, 1132, 660]
    draw.rounded_rectangle(bubble_box, radius=26, fill=(255, 255, 255),
                           outline=(0, 0, 0), width=4)
    # Little tail pointing down towards the ghost.
    draw.polygon([(800, 656), (842, 656), (806, 700)], fill=(255, 255, 255))
    draw.line([(800, 656), (806, 700)], fill=(0, 0, 0), width=4)
    draw.line([(842, 656), (806, 700)], fill=(0, 0, 0), width=4)
    bubble_font = load_font(36)
    draw.text((772, 570), "we got paid", font=bubble_font, fill=(20, 20, 20))
    draw.text((772, 612), "while you waited", font=bubble_font, fill=(20, 20, 20))


def build_meme():
    """Assemble the whole scene and save it as meme.png."""
    image = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw_sunset_sky(draw, CANVAS_SIZE, CANVAS_SIZE)
    draw_sun(draw)
    draw_skyline(draw)
    draw_beach(draw, CANVAS_SIZE)
    draw_palm_tree(draw, 118, 900, 58)
    draw_palm_tree(draw, 1082, 900, -58)
    draw_bench(draw)
    draw_gamer(draw)
    draw_makefun_ghost(draw)
    draw_speech_bubble(draw)
    draw_caption(draw, CANVAS_SIZE)
    image.save(OUTPUT_PATH, format="PNG")
    print(f"saved {OUTPUT_PATH} {image.size[0]}x{image.size[1]}")


if __name__ == "__main__":
    build_meme()
