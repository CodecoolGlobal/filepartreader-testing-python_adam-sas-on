import os
import curses
import analyzer

def files_in_dir(path):
	files = []

	with os.scandir(path) as files_dir:
		for file_dir in files_dir:
			if file_dir.is_file():
				files.append(file_dir.name)

	return files
#

def list_files(stdscr, files, i_begin, i_current, row_begin):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	scr_height,i = stdscr.getmaxyx()

	i = i_begin
	j = 0
	while i < len(files) and j < scr_height:
		if i == i_current:
			stdscr.addstr(j+row_begin, 4, files[i], curses.A_BOLD)
		else:
			stdscr.addstr(j+row_begin, 4, files[i])
		i += 1
		j += 1
	#
#

def select_file(stdscr, dir_path="resources/"):
	files = files_in_dir(dir_path)
	if len(files) < 1:
		return ""

	stdscr.move(1, 0)
	stdscr.clrtobot()
	stdscr.addstr(1, 4, "Select file to analyze from the list ")

	file_no = 0
	file_1st = 0
	run = True
	row_0 = 3

	while run:
		scr_height,i = stdscr.getmaxyx()
		list_files(stdscr, files, file_1st, file_no, row_0)

		c = stdscr.getch()

		if c == curses.KEY_UP:
			if file_no > 0:
				file_no -= 1
				if file_no <= file_1st and file_1st > 0:
					file_1st = file_no - 1 if file_no > 1 else 0 # file_no > 1 file_no - 1 : 0
			if scr_height > len(files):
				file_1st = 0
		elif c == curses.KEY_DOWN:
			if file_no < len(files):
				if file_no + 1 < len(files):
					file_no += 1

				i = file_no + 1 - file_1st
				if i >= scr_height:
					i = file_no + 1 - scr_height
					file_1st = i + 1 if file_no < len(files) else i
			if scr_height > len(files):
				file_1st = 0
		if c == curses.KEY_ENTER or c==10:
			run = False
	#

	stdscr.move(1, 0)
	stdscr.clrtobot()

	return files[file_no]
#

def main_menu(stdscr, selected, row_begin=2, case_sensitive=True, unique=False):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	menus = ["1. select file to analyze", "2. set read range"]
	if case_sensitive:
		menus.append("[x] case sensitive")
	else:
		menus.append("[ ] case sensitive")

	if unique:
		menus.append("[x] uniqueness")
	else:
		menus.append("[ ] uniqueness")

	menus.append("q. exit")

	row = row_begin
	i = 0
	for menu in menus:
		if selected == i:
			stdscr.addstr(row, 2, menu, curses.A_BOLD)
		else:
			stdscr.addstr(row, 2, menu)
		i += 1
		row += 1
	#
	return i
#

def run(stdscr):
	stdscr = curses.initscr()

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)

	selected_file = ""
	case_sensitive = True
	words_uniqueness = False

	cmd = 0
	run = True
	stdscr.addstr(0, 1, "  Filepartreader testing")

	while run:
		if len(selected_file):
			stdscr.addstr(1, 7, "Analysis  {}".format(selected_file) )

		menu_len = main_menu(stdscr, cmd)

		c = stdscr.getch()

		if cmd == 0 and (c == curses.KEY_ENTER or c==10):
			selected_file = select_file(stdscr)
		elif cmd == menu_len-1 and (c == curses.KEY_ENTER or c==10):
			run = False
		elif c == curses.KEY_UP and cmd > 0:
			cmd -= 1
		elif c == curses.KEY_DOWN and cmd < menu_len-1:
			cmd += 1
		elif c == ord('1'):
			cmd = 0
		elif c == ord('q'):
			cmd = menu_len - 1
	#

	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()

	curses.endwin()
#

if __name__ == '__main__':
	curses.wrapper(run)

