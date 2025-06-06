from PIL import Image
from renderer import *
import shutil
import curses
import sys


W, _ = shutil.get_terminal_size()
even = W % 2 == 0

bg_img = Image.open('bg.jpeg')
bg_img = bg_img.resize((W, W if even else W-1))
window = load_sprite(bg_img)

sprite_img = Image.open('sprite.png')
sprite = load_sprite(sprite_img)
blit_sprite(window, sprite, 10, 10)
frame = get_string(window)
H = len(frame)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    write = sys.stdout.write  # local alias for speed
    flush = sys.stdout.flush
    
    esc_home = "\033[H"
    esc_reset = "\033[0m"
    info = f"{esc_reset}window size: {W} : {H}\n"

    timer = 0
    while True:
        timer += 1
        key = stdscr.getch()
        if key == ord('q'):
            break

        frame = get_string(blit_sprite(window, sprite, 10, timer))

        write(esc_home)
        write(''.join(frame))
        write(info)
        flush()

        stdscr.refresh()


curses.wrapper(main)