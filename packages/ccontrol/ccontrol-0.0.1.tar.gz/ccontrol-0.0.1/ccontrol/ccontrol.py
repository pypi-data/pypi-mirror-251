import curses
from typing import Any

# Define color constants for clarity and ease of use
WHITE:			int = 1
RED:			int = 2
YELLOW:			int = 3
GREEN:			int = 4
BLUE:			int = 5
CYAN:			int = 6
MAGENTA:		int = 7

# Define attribute constants for different text styles
NORMAL:			int = curses.A_NORMAL
BOLD:			int = curses.A_BOLD
UNDERLINE:		int = curses.A_UNDERLINE
REVERSE:		int = curses.A_REVERSE
BLINK:			int = curses.A_BLINK

def text(
	stdscr: 'curses._CursesWindow', 
	x:			int, 
	y:			int, 
	text:		str, 
	color_pair: int = 1, 
	style:		int = curses.A_NORMAL
) -> bool:
	"""
	Outputs text at a given position with specified color and style.

	:param stdscr:		The window object on which to output the text.
	:param x:			The x-coordinate (column) of the first character of text.
	:param y:			The y-coordinate (row) of the first character of text.
	:param text:		The string of text to output.
	:param color_pair:  The color pair to use for the text.
	:param style:		The styling attribute(s) to apply to the text.
	:return:				True if the text was added successfully, False otherwise.
	"""
	try:
		stdscr.addstr(y, x, text, curses.color_pair(color_pair) | style)
		return True
	except curses.error:
		return False

def initialize_screen(
	colors:	  bool = True, 
	hide_cursor: bool = True, 
	timeout:	 bool = True, 
	get_keypad:  bool = True, 
	echo_off:	 bool = True, 
	clear_text:  bool = True
) -> 'curses._CursesWindow':
	"""
	Initializes the curses screen with custom settings.

	:param hide_cursor: Boolean, if True the cursor will be hidden.
	:param timeout:	Boolean, if True the screen will have a timeout.
	:param get_keypad:  Boolean, if True the keypad will be enabled.
	:param echo_off:	Boolean, if True the echo will be disabled.
	:param clear_text:  Boolean, if True the text input will immediately be executed without wait for Enter key.
	:return:				The initialized window object (stdscr).
	"""
	
	# Initialize curses window which begins the curses mode
	stdscr = curses.initscr()

	# Start color functionality
	if colors:
		curses.start_color()
		curses.use_default_colors()

		# Initialize color pairs with foreground and background colors
		curses.init_pair(WHITE,   curses.COLOR_WHITE,   curses.COLOR_BLACK)
		curses.init_pair(RED,	 curses.COLOR_RED,	 curses.COLOR_BLACK)
		curses.init_pair(YELLOW,  curses.COLOR_YELLOW,  curses.COLOR_BLACK)
		curses.init_pair(GREEN,   curses.COLOR_GREEN,   curses.COLOR_BLACK)
		curses.init_pair(BLUE,	curses.COLOR_BLUE,	curses.COLOR_BLACK)
		curses.init_pair(CYAN,	curses.COLOR_CYAN,	curses.COLOR_BLACK)
		curses.init_pair(MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	
	# Hide the cursor if hide_cursor is True
	if hide_cursor:  
		curses.curs_set(0)
	
	# Set the window timeout to 0 if timeout is True, making it non-blocking
	if timeout:
		stdscr.timeout(0)
	
	# Allows the use of keys like Home, Page Up, and arrows if get_keypad is True
	if get_keypad:
		stdscr.keypad(True)
	
	# Turn off auto echo of keys to the screen if echo_off is True
	if echo_off: 
		curses.noecho()
	
	# React to keys instantly without requiring the Enter key; pass them to the program if clear_text is True
	if clear_text:
		curses.cbreak()
	
	# Return the initialized curses window object
	return stdscr

def input_box(
	stdscr: 'curses._CursesWindow',
	x:          int,
	y:          int,
	width:      int,
	title:      str = "",
	color_pair: int = 1,
	style:      int = curses.A_NORMAL
) -> str:
	"""
	Creates an input box for user to enter text.

	:param stdscr: The window object to create the input box in.
	:param x: The x-coordinate (column) to start the input box.
	:param y: The y-coordinate (row) to start the input box.
	:param width: The width of the input box.
	:param title: The title of the input box.
	:param color_pair: The color pair to use for the input box.
	:param style: The styling attribute(s) to apply to the input box.
	:return: The string input by the user.
	"""

	curses.echo()  # Enable echoing of characters
	curses.curs_set(1)  # Show cursor
	stdscr.attron(curses.color_pair(color_pair) | style)

	# Draw a box
	stdscr.addch(y, x - 1, curses.ACS_VLINE)
	stdscr.addch(y, x + width, curses.ACS_VLINE)

	for _x in range(x, x + width):
		stdscr.addch(y - 1, _x, curses.ACS_HLINE)
		stdscr.addch(y + 1, _x, curses.ACS_HLINE)

	stdscr.addch(y - 1, x - 1, curses.ACS_ULCORNER)
	stdscr.addch(y - 1, x + width, curses.ACS_URCORNER)
	stdscr.addch(y + 1, x - 1, curses.ACS_LLCORNER)
	stdscr.addch(y + 1, x + width, curses.ACS_LRCORNER)
	# Draw a title (if provided)
	if title:
		stdscr.addstr(y - 1, x, title)

	input_str = ""
	cursor_x = x
	while True:
		stdscr.move(y, cursor_x)  # Move the cursor to the current position
		stdscr.refresh()

		key = stdscr.getch()  # Get user input
		if key in [curses.KEY_BACKSPACE, 127, 8]:  # Handle backspace
			if cursor_x > x:
				cursor_x -= 1  # Decrement the cursor position
				input_str = input_str[:-1]  # Remove the last character from the input string
				stdscr.move(y, cursor_x)  # Move the cursor to the new position
				stdscr.addch(y, cursor_x, ' ')  # Remove the character from the screen
		elif key in {10, 13}:  # Enter key pressed (newline or carriage return)
			break
		else:
			if cursor_x < x + width - 1:  # Ensure the cursor doesn't go outside the box
				char = chr(key)
				input_str += char
				stdscr.addch(y, cursor_x, char)
				cursor_x += 1

	stdscr.attroff(curses.color_pair(color_pair) | style)
	curses.curs_set(0)  # Hide cursor again
	curses.noecho()  # Turn off echoing of characters

	# Return the user's input
	return input_str.strip()

def get_key(
	stdscr: 'curses._CursesWindow'
) -> int:
    """
    Waits for a user key press and returns the key's keycode.

    :param stdscr: The window object which captures the key press.
    :return: The key's integer keycode.
    """
    key = stdscr.getch()  # Wait for user input and return the key's integer keycode
    return key

def exit_programm():
	curses.endwin()