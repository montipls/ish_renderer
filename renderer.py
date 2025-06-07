from PIL import Image
import copy


precomputed_chars = {}
for fg in range(256):
    for bg in range(256):
        precomputed_chars[(fg, bg)] = f"\033[38;5;{fg}m\033[48;5;{bg}m▄"


def rgb_to_256(r, g, b):
    r_ = int(r / 256 * 6)
    g_ = int(g / 256 * 6)
    b_ = int(b / 256 * 6)

    r_ = min(r_, 5)
    g_ = min(g_, 5)
    b_ = min(b_, 5)

    return 16 + 36 * r_ + 6 * g_ + b_


def load_sprite(img: Image) -> list[list[int]]:
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


def blit_sprite(surface: list[list[int]], sprite: list[list[int]], x: int, y: int) -> list[list[int]]:
    result = surface[:]
    H = len(surface)
    W = len(surface[0])
    sh = len(sprite)
    sw = len(sprite[0])

    valid_sy_start = max(0, -y)
    valid_sy_end = min(sh, H - y)
    valid_sx_start = max(0, -x)
    valid_sx_end = min(sw, W - x)

    copied_rows = set()

    for sy in range(valid_sy_start, valid_sy_end):
        py = y + sy
        if py not in copied_rows:
            result[py] = surface[py][:]
            copied_rows.add(py)
        row = result[py]
        for sx in range(valid_sx_start, valid_sx_end):
            px = x + sx
            pixel = sprite[sy][sx]
            if pixel:
                row[px] = pixel

    return result


def get_string(surface: list[list[int]]) -> str:
    W = len(surface[0])
    H = len(surface)
    pc = precomputed_chars
    
    output_lines = []
    outpend = output_lines.append
    for y in range(0, H, 2):
        line_chars = []
        append = line_chars.append

        for x in range(W):
            bg = surface[y][x]
            fg = surface[y+1][x]

            append(pc[(fg, bg)])
        outpend(''.join(line_chars))
    return ''.join(output_lines)
