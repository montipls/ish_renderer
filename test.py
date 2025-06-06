from PIL import Image
from renderer import *
import shutil
import curses


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

        blit_sprite(window, sprite, 10, timer)
        frame = get_string(window)

        for y, line in enumerate(frame):
            stdscr.addstr(y, 0, line[:W])

        stdscr.addstr(H, 0, f"window size: {W} : {H}")
        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break


curses.wrapper(main)