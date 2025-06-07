from PIL import Image
from renderer import *
import shutil
import curses
import sys
import time


W, _ = shutil.get_terminal_size()
even = W % 2 == 0
size = (W, W if even else W-1)

bg_img = Image.open('bg.jpeg')
bg_img = bg_img.resize(size)
window = load_sprite(bg_img)

sprite_img = Image.open('sprite.png')
sprite_size = sprite_img.size
sprite = load_sprite(sprite_img)
H = size[1]


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    write = sys.stdout.write
    flush = sys.stdout.flush

    esc_home = "\033[H"
    esc_reset = "\033[0m"
    info = f"{esc_reset}window size: {W}:{H}"

    x = 0
    y = 0
    x_vel = 1
    y_vel = 0
    last_key = -1
    key = -1
    last_time = time.time()

    while True:
        if last_key != -1:
            while key == last_key:
                key = stdscr.getch()
        else:
            key = stdscr.getch()
        if key == ord('q'):
            break
        
        lw = x <= 0
        rw = x + sprite_size[0] >= W
        bw = y + sprite_size[1] >= H
        tw = y <= 0

        if key == 260:
            x_vel = -1
            y_vel = 0
        if key == 261:
            x_vel = 1
            y_vel = 0
        if key == 258:
            x_vel = 0
            y_vel = 1
        if key == 259:
            x_vel = 0
            y_vel = -1

        last_key = key
        if lw and x_vel < 0:
            pass
        elif rw and x_vel > 0:
            pass
        else:
            x += x_vel

        if tw and y_vel < 0:
            pass
        elif bw and y_vel > 0:
            pass
        else:
            y += y_vel

        now = time.time()
        dt = now - last_time
        last_time = now
        fps = 1 / dt

        frame = get_string(blit_sprite(window, sprite, x, y))

        write(esc_home)
        write(frame)
        write(info + '\r\n')
        write(f"fps: {fps:.1f}\r\n")
        write(f"wall collision: {'1' if lw or rw or tw or bw else '0'}\r\n")
        write(f"position (top-left): {x}, {y}")
        write("\033[J")
        flush()

        stdscr.refresh()


curses.wrapper(main)
