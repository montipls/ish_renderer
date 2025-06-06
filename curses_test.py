import curses

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    stdscr.nodelay(True)

    i = 0
    while True:
        stdscr.bkgd(' ', curses.color_pair(1 if i % 2 == 0 else 2))
        stdscr.clear()
        stdscr.refresh()
        i += 1
        if stdscr.getch() != -1:
            break

curses.wrapper(main)
