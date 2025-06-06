from PIL import Image
import numpy as np


def load_sprite(img: Image) -> np.ndarray:
    arr = np.array(img, dtype=np.uint8)
    
    alpha_channel = arr[:, :, 3]
    arr[:, :, 3] = (alpha_channel > 0).astype(np.uint8)
    
    return arr


def blit_sprite(surface: np.ndarray, sprite: np.ndarray, x: int, y: int) -> None:
    sh, sw, _ = sprite.shape
    H, W, _ = surface.shape

    x_start_sprite = max(0, -x)
    y_start_sprite = max(0, -y)
    x_start_surface = max(0, x)
    y_start_surface = max(0, y)

    x_end_surface = min(W, x + sw)
    y_end_surface = min(H, y + sh)

    sprite_w = x_end_surface - x_start_surface
    sprite_h = y_end_surface - y_start_surface

    if sprite_w <= 0 or sprite_h <= 0:
        return

    sprite_part = sprite[y_start_sprite:y_start_sprite + sprite_h, x_start_sprite:x_start_sprite + sprite_w]
    surface_part = surface[y_start_surface:y_end_surface, x_start_surface:x_end_surface]

    alpha = sprite_part[:, :, 3].astype(bool)
    surface_part[alpha] = sprite_part[alpha][:, :3]


def get_string(surface: np.ndarray) -> list[str]:
    H, W, _ = surface.shape

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