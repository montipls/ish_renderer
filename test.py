from PIL import Image
from renderer import *
import shutil


_, rows = shutil.get_terminal_size()

bg_img = Image.open('bg.jpeg')
bg_img = bg_img.resize((rows, rows))
window = load_sprite(bg_img)

sprite_img = Image.open('sprite.png')
sprite = load_sprite(sprite_img)
blit_sprite(window, sprite, 0, 0)

frame = get_string(window)
print('\n'.join(frame))
