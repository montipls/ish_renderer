from PIL import Image
import copy


def rgb_to_256(r, g, b):
    r_ = int(r / 256 * 6)
    g_ = int(g / 256 * 6)
    b_ = int(b / 256 * 6)

    r_ = min(r_, 5)
    g_ = min(g_, 5)
    b_ = min(b_, 5)

    return 16 + 36 * r_ + 6 * g_ + b_


def load_sprite(img: Image) -> list[list[list[int]]]:
    img = img.convert("RGBA")
    width, height = img.size
    pixels = img.load()

    result = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = pixels[x, y]
            row.append(rgb_to_256(r, g, b) if a > 0 else None)
        result.append(row)
    return result


def blit_sprite(surface, sprite, x, y):
    H = len(surface)
    W = len(surface[0])
    sh = len(sprite)
    sw = len(sprite[0])

    result = surface[:]
    rows_copied = {}

    for sy in range(sh):
        py = y + sy
        if py < 0 or py >= H:
            continue

        if py not in rows_copied:
            result[py] = surface[py][:]
            rows_copied[py] = True

        row = result[py]

        for sx in range(sw):
            px = x + sx
            if px < 0 or px >= W:
                continue

            pixel = sprite[sy][sx]
            if pixel:
                row[px] = pixel

    return result


def get_string(surface: list[list[list[int]]]) -> list[str]:
    H = len(surface)
    W = len(surface[0])

    output_lines = []
    outpend = output_lines.append

    fg_prefix = "\033[38;5;"
    bg_prefix = "m\033[48;5;"
    suffix = "m▄"

    for y in range(0, H, 2):
        line_chars = []
        append = line_chars.append

        for x in range(W):
            bg = surface[y][x]
            fg = surface[y+1][x]

            append(fg_prefix)
            append(str(fg))
            append(bg_prefix)
            append(str(bg))
            append(suffix)

        outpend(''.join(line_chars))
    return output_lines