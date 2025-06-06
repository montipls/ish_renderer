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


def blit_sprite(surface: list[list[list[int]]], sprite: list[list[list[int]]], x: int, y: int) -> list[list[list[int]]]:
    result = copy.deepcopy(surface)
    H = len(result)
    W = len(result[0])
    sh = len(sprite)
    sw = len(sprite[0])

    for sy in range(sh):
        py = y + sy
        if py < 0 or py >= H:
            continue
        for sx in range(sw):
            px = x + sx
            if px < 0 or px >= W:
                continue
            pixel = sprite[sy][sx]
            if pixel:
                result[py][px] = pixel

    return result


def get_string(surface: list[list[list[int]]]) -> list[str]:
    H = len(surface)
    W = len(surface[0])

    output_lines = []
    for y in range(0, H, 2):
        line_chars = []
        for x in range(W):
            bg = surface[y][x]
            fg = surface[y+1][x]

            char = f"\033[38;5;{fg}m\033[48;5;{bg}m▄"
            line_chars.append(char)
        output_lines.append(''.join(line_chars))
    return output_lines