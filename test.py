from PIL import Image
from renderer import *
import shutil


_, rows = shutil.get_terminal_size()

img = Image.open('bg.jpeg')
img = img.resize((rows, rows))
window = load_sprite(img)

sprite = Image.open('sprite.jpeg')
blit_sprite(window, sprite, 0, 0)

frame = get_string(window)
print('\n'.join(frame))
