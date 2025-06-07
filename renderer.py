from PIL import Image
import copy


palette = ['\033[38;5;{0}m\033[48;5;{1}m▄'.format(fg, bg) for fg in range(256) for bg in range(256)]
fgpalette = [f"\033[38;5;{i}m▄" for i in range(256)]
bgpalette = [f"\033[48;5;{i}m▄" for i in range(256)]


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

    copied = [False] * H

    for sy in range(valid_sy_start, valid_sy_end):
        py = y + sy
        if not copied[py]:
            result[py] = surface[py][:]
            copied[py] = True
        row = result[py]
        sprite_row = sprite[sy]
        for sx in range(valid_sx_start, valid_sx_end):
            px = x + sx
            pixel = sprite_row[sx]
            if pixel and row[px] != pixel:
                row[px] = pixel

    return result


def get_string(surface: list[list[int]]) -> str:
    W = len(surface[0])
    H = len(surface)

    p = palette
    fgp = fgpalette
    bgp = bgpalette
    
    output_lines = []
    outpend = output_lines.append
    for y in range(0, H, 2):
        line_chars = []
        append = line_chars.append
        
        last_fg = -1
        last_bg = -1
        
        row0 = surface[y]
        row1 = surface[y+1]

        for x in range(W):
            bg = row0[x]
            fg = row1[x]

            if fg != last_fg and bg != last_bg:
                append(p[(fg << 8) | bg])
                last_fg, last_bg = fg, bg
            elif fg != last_fg:
                append(fgp[fg])
                last_fg = fg
            elif bg != last_bg:
                append(bgp[bg])
                last_bg = bg
            else:
                append('▄')

        outpend(''.join(line_chars))
    return ''.join(output_lines)
