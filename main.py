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


def run(stdscr):
	stdscr = curses.initscr()

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)

	selected_file = ""

	cmd = 0
	run = True
	stdscr.addstr(0, 1, "  Filepartreader testing")

	while run:
		file_to_analyze = select_file(stdscr)
		stdscr.addstr(2, 1, file_to_analyze)

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

