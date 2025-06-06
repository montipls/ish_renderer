from PIL import Image
from renderer import *
import shutil
import curses
import sys


W, H = shutil.get_terminal_size()
even = W % 2 == 0

bg_img = Image.open('bg.jpeg')
bg_img = bg_img.resize((W, W if even else W-1))
window = load_sprite(bg_img)

sprite_img = Image.open('sprite.png')
sprite = load_sprite(sprite_img)
blit_sprite(window, sprite, 10, 10)
frame = get_string(window)
W = len(frame[0])
H = len(frame)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    timer = 0
    while True:
        timer += 1
        key = stdscr.getch()
        if key == ord('q'):
            break

        blit_sprite(window, sprite, 10, timer)
        frame = get_string(window)

        sys.stdout.write("\033[H")  # move cursor to top-left
        sys.stdout.write('\n'.join(frame) + '\n')
        sys.stdout.write(f"window size: {W} : {H}\n")
        sys.stdout.flush()
        
        stdscr.refresh()


curses.wrapper(main)