from typing import NamedTuple

class Color(NamedTuple):
	"""
	Defines a 'Color' type for type hinting.
	"""
	red: int
	green: int
	blue: int

def colorSprintf(text: str, c: Color) -> str:
	"""
	Returns a string that will print in the specified color, by wrapping it in ANSI control codes
	"""
	return f"\033[38;2;{c.red};{c.green};{c.blue}m{text}\033[m"

def colorSprintfBckgrnd(text: str, bgcolor: Color, fgcolor: Color=Color(255, 255, 255)) -> str:
	"""
	Returns a string that will print with the given background (and optionally foreground) color(s)
	"""
	return "\033[48;2;%d;%d;%dm\033[38;2;%d;%d;%dm%s\033[m" % (bgcolor[0], bgcolor[1], bgcolor[2],
	                                                           fgcolor[0], fgcolor[1], fgcolor[2],
	                                                           text)
