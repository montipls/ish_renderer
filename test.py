from PIL import Image
from renderer import *
import shutil
import curses
import sys
import time


W, _ = shutil.get_terminal_size()
even = W % 2 == 0
size = (W, W if even else W-1)

bg_img = Image.open('bg.png')
bg_img = bg_img.resize(size)
window = load_mono_sprite(bg_img)

sprite_img = Image.open('sprite.png')
sprite_size = sprite_img.size
sprite = load_mono_sprite(sprite_img)
mono_sprite_data = get_mono_data(sprite)
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
        now = time.time()
        dt = now - last_time
        last_time = now
        fps = 1 / dt

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

        frame = get_mono_string(rgb_to_256(255, 255, 255), rgb_to_256(0, 0, 0), blit_mono_sprite(window, mono_sprite_data, x, y))

        write(esc_home)
        write(frame)
        write(info + '    \r\n')
        write(f"buffer length: {len(frame)}    \r\n")
        write(f"fps: {fps:.1f}    \r\n")
        write(f"wall collision: {'1' if lw or rw or tw or bw else '0'}    \r\n")
        write(f"position (top-left): {x}, {y}    \r\n")
        flush()

        stdscr.refresh()

        elapsed = time.time() - now
        sleep_time = 1/30 - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)


curses.wrapper(main)
