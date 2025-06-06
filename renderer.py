from PIL import Image
import numpy as np


def load_sprite(img: Image) -> list[list[list[int]]]:
    img = img.convert("RGBA")
    width, height = img.size
    pixels = img.load()

    result = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = pixels[x, y]
            a = 1 if a > 0 else 0
            row.append([r, g, b, a])
        result.append(row)
    return result


def blit_sprite(surface: list[list[list[int]]], sprite: list[list[list[int]]], x: int, y: int) -> None:
    H = len(surface)
    W = len(surface[0])
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
            if pixel[3] != 0:
                surface[py][px][0] = pixel[0]
                surface[py][px][1] = pixel[1]
                surface[py][px][2] = pixel[2]


def get_string(surface: list[list[list[int]]]) -> list[str]:
    H = len(surface)
    W = len(surface[0])

    output_lines = []
    for y in range(0, H, 2):
        line_chars = []
        for x in range(W):
            bg = surface[y][x]
            fg = surface[y+1][x]

            char = f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m\033[48;2;{bg[0]};{bg[1]};{bg[2]}m▄\033[0m"
            line_chars.append(char)
        output_lines.append(''.join(line_chars))
    return output_lines