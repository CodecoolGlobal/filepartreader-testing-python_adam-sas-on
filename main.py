import os
import curses
from reader import FilePartReader
from analyzer import FileAnalyzer

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

def set_range(stdscr, current_range, upper_limit, row_begin=2):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	stdscr.addstr(row_begin, 4, "Range of analysis: ")

	menus = ["Beginning of the range: {}", "End of the range: {}", "Quit"]

	digits={ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9')}

	local_range = [current_range[0], current_range[1]]
	ind = 0
	run = True
	while run:
		row = row_begin + 1
		stdscr.addstr(row, 2, menus[0].format(local_range[0]))
		row += 1
		stdscr.addstr(row, 2, menus[1].format(local_range[1]))
		row += 1
		stdscr.addstr(row, 2, menus[2])

		if ind == 0 or ind == 1:
			stdscr.move(row_begin + 1 + ind, 0)
			stdscr.clrtoeol()
			if ind == 0:
				stdscr.addstr(row_begin + 1, 2, menus[0].format(local_range[0]), curses.A_BOLD)
			else:
				stdscr.addstr(row_begin + 2, 2, menus[1].format(local_range[1]), curses.A_BOLD)
		else:
			stdscr.addstr(row_begin + len(menus), 2, menus[-1], curses.A_BOLD)

		c = stdscr.getch()

		if c == curses.KEY_UP and ind > 0:
			ind -= 1
		elif c == curses.KEY_DOWN and ind < 2:
			ind += 1
		elif ind == 2 and (c == curses.KEY_ENTER or c==10):
			run = False
		elif c == curses.KEY_BACKSPACE and (ind == 0 or ind == 1):
			local_range[ind] = local_range[ind]//10
			if local_range[1] < local_range[0]:
				local_range[1] = local_range[0]
		elif c in digits and (ind == 0 or ind == 1):
			nr = int(c - ord('0'))
			if ind == 0:
				local_range[0] = local_range[0]*10 + nr
				if local_range[0] > local_range[1]:
					local_range[0] = local_range[1]
			elif ind == 1:
				local_range[1] = local_range[1]*10 + nr
				if local_range[1] > upper_limit:
					local_range[1] = upper_limit
	#
	return (local_range[0], local_range[1])
#

def analyzer_menu(stdscr, selected, substring, row_begin=3):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	menus = ["1. get words ordered alphabetically", "2. get strings which palindromes", "3. get words containing substring: \"" + substring + "\"", "q. exit"]

	row = row_begin
	for menu in menus:
		stdscr.addstr(row, 2, menu)
		row += 1
	#
	if selected >= 0 and selected < len(menus):
		row = row_begin + selected
		stdscr.addstr(row, 2, menus[selected], curses.A_BOLD)
#

def analyze_file(stdscr, analyzer_class: FileAnalyzer, row_begin=2):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	stdscr.addstr(row_begin, 3, "Range of analysis: ")

	chars = {ord('a')}
	substring = ""

	cmd = 0
	run = True
	while run:
		analyzer_menu(stdscr, cmd, substring)

		c = stdscr.getch()

		if cmd == 0 and (c == curses.KEY_ENTER or c==10):
			pass
		elif cmd == 1 and (c == curses.KEY_ENTER or c==10):
			pass
		elif cmd == 2 and c != curses.KEY_UP and c != curses.KEY_DOWN:
			if c == curses.KEY_ENTER or c==10:
				pass
			elif c == curses.KEY_BACKSPACE and len(substring) > 0:
				substring = substring[:-1]
			elif c in chars:
				substring += str(c)
		elif (cmd == 3 and (c == curses.KEY_ENTER or c==10) ) or c == curses.KEY_EXIT:
			run = False
		elif c == curses.KEY_UP and cmd > 0:
			cmd -= 1
		elif c == curses.KEY_DOWN and cmd < 3:
			cmd += 1
	#

#

def main_menu(stdscr, selected, file_to_analyze, case_sensitive=True, unique=False, row_begin=2):
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

	if len(file_to_analyze):
		menus.append("3. Analyze  {}".format(file_to_analyze))

	menus.append("q. exit")

	row = row_begin
	i = 0
	for menu in menus:
		stdscr.addstr(row, 2, menu)
		row += 1
		i += 1
	#

	if selected >= 0 and selected < len(menus):
		row = row_begin + selected
		stdscr.addstr(row, 2, menus[selected], curses.A_BOLD)

	return i
#

def run(stdscr):
	stdscr = curses.initscr()

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)

	dir_path = "resources/"
	selected_file = ""
	case_sensitive = True
	words_uniqueness = False
	check_keys = {curses.KEY_STAB, curses.KEY_ENTER, 10, curses.KEY_MARK, curses.KEY_SELECT, ' ', ord(' ')}

	reader = FilePartReader()
	analyzer = FileAnalyzer(reader)

	cmd = 0
	run = True
	stdscr.addstr(0, 1, "  Filepartreader testing")

	while run:
		if len(selected_file):
			stdscr.addstr(1, 7, "Analysis  {}".format(selected_file) )

		menu_len = main_menu(stdscr, cmd, selected_file, case_sensitive, words_uniqueness)

		c = stdscr.getch()

		if cmd == 0 and (c == curses.KEY_ENTER or c==10):
			selected_file = select_file(stdscr)
			reader.setup(dir_path + selected_file, 1, -1)
		elif cmd == 1 and (c == curses.KEY_ENTER or c==10):
			upper_limit = reader.lines_in_file()
			read_range = set_range(stdscr, reader.get_read_range(), upper_limit)
			reader.set_read_range(read_range[0], read_range[1])
		elif (cmd == menu_len-1 and (c == curses.KEY_ENTER or c==10) ) or c == curses.KEY_EXIT:
			run = False
		elif c == curses.KEY_UP and cmd > 0:
			cmd -= 1
			if cmd == 1 and len(selected_file) < 1:
				cmd = 0
		elif c == curses.KEY_DOWN and cmd < menu_len-1:
			cmd += 1
			if cmd == 1 and len(selected_file) < 1:
				cmd += 1
		elif c == ord('1'):
			cmd = 0
		elif cmd == 2 and c in check_keys:
			case_sensitive = False if case_sensitive else True
		elif cmd == 3 and c in check_keys:
			words_uniqueness = False if words_uniqueness else True
		elif cmd == menu_len-2 and len(selected_file):
			analyze_file(stdscr, analyzer)
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

