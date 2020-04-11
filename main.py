import curses
import analyzer


def run(stdscr):
	stdscr = curses.initscr()

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)

	run = True
	stdscr.addstr(1, 1, "  Filepartreader testing")

	while run:
		c = stdscr.getch()
		run = False
	#

	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()

	curses.endwin()
#

if __name__ == '__main__':
	curses.wrapper(run)

