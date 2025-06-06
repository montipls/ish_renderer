from PIL import Image
from renderer import *
import shutil


x, _ = shutil.get_terminal_size()
even = x % 2 == 0
print(x)

bg_img = Image.open('bg.jpeg')
bg_img = bg_img.resize((x, x if even else x-1))
window = load_sprite(bg_img)

sprite_img = Image.open('sprite.png')
sprite = load_sprite(sprite_img)
blit_sprite(window, sprite, 10, 10)

frame = get_string(window)
print('\n'.join(frame))
