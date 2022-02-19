"""
color.py
========

Usage
-----

>>> import color
>>>
>>> # 8-bit color
>>> print(red('red') + green('green') + blue('blue'))
>>> print(bold(yellow('bold yellow')) + underline(cyan('underline cyan')))
>>> print(magenta_hl('magenta highlight'))
>>>
>>> # xterm 256 color
>>> print(bg256('A9D5DE', fg256('276F86', 'Info!')))
>>> print(bg256('E0B4B4', fg256('912D2B', 'Warning!')))
>>> print(hl256('10a3a3', 'Teal'))

Note:

1. Every color function receives and returns string, so that the result
   could be used with any other strings, in any string formatting situation.

2. If you pass a str type string, the color function will return a str.
   If you pass a bytes type string, the color function will return a bytes string.

3. Color functions could be composed together, like put ``red`` into ``bold``,
   or put ``bg256`` into ``fg256``. ``xxx_hl`` and ``hl256`` are mostly used
   independently.

API
---

8-bit colors:

========  ============  ===========
 Colors    Background    Highlight
========  ============  ===========
black     black_bg      black_hl
red       red_bg        red_hl
green     green_bg      green_hl
yellow    yellow_bg     yellow_hl
blue      blue_bg       blue_hl
magenta   magenta_bg    magenta_hl
cyan      cyan_bg       cyan_hl
white     white_bg      white_hl
========  ============  ===========

Styles:
- bold
- italic
- underline
- strike
- blink

.. py:function:: <color_function>(s)

   Decorate string with specified color or style.

   A color function with ``_bg`` suffix means it will set color as background.
   A color function with ``_hl`` suffix means it will set color as background,
   and change the foreground as well to make the word standout.

   :param str s: The input string
   :return: The decorated string
   :rtype: string
   :raises ValueError: if the message_body exceeds 160 characters


256 colors:
- fg256
- bg256
- hl256

.. py:function:: <256_color_function>(hexrgb, s)

   Decorate string with specified hex rgb color

   ``fg256`` will set color as foreground.
   ``bg256`` will set color as background.
   ``hg256`` will highlight input with the color.

   :param str hexrgb: The hex rgb color string, accept length 3 and 6. eg: ``555``, ``912D2B``
   :param str s: The input string
   :return: The decorated string
   :rtype: string
   :raises ValueError: If the input string's length not equal to 3 or 6.
"""

from typing import Union, Any, Callable, Optional, Tuple, List, Dict
import sys


_use_color_no_tty = True


def use_color_no_tty(flag):
    global _use_color_no_tty
    _use_color_no_tty = flag


def use_color():
    if sys.stdout.isatty():
        return True
    if _use_color_no_tty:
        return True
    return False


def esc(*codes: Union[int, str]) -> str:
    """Produces an ANSI escape code from a list of integers
    :rtype: text_type
    """
    return t_('\x1b[{}m').format(t_(';').join(t_(str(c)) for c in codes))


def t_(b: Union[bytes, Any]) -> str:
    """ensure text type"""
    return b.decode() if isinstance(b, bytes) else b


def b_(t: Union[str, Any]) -> bytes:
    """ensure binary type"""
    return t.encode() if isinstance(t, str) else t


###############################################################################
# 8 bit Color
###############################################################################

def make_color(start, end: str) -> Callable[[str], str]:
    def color_func(s: str) -> str:
        return s if not use_color() else start + t_(s) + end

    return color_func


# According to https://en.wikipedia.org/wiki/ANSI_escape_code#graphics ,
# 39 is reset for foreground, 49 is reset for background, 0 is reset for all
# we can use 0 for convenience, but it will make color combination behaves weird.
END = esc(0)

FG_END = esc(39)
black = make_color(esc(30), FG_END)
red = make_color(esc(31), FG_END)
green = make_color(esc(32), FG_END)
yellow = make_color(esc(33), FG_END)
blue = make_color(esc(34), FG_END)
magenta = make_color(esc(35), FG_END)
cyan = make_color(esc(36), FG_END)
white = make_color(esc(37), FG_END)

BG_END = esc(49)
black_bg = make_color(esc(40), BG_END)
red_bg = make_color(esc(41), BG_END)
green_bg = make_color(esc(42), BG_END)
yellow_bg = make_color(esc(43), BG_END)
blue_bg = make_color(esc(44), BG_END)
magenta_bg = make_color(esc(45), BG_END)
cyan_bg = make_color(esc(46), BG_END)
white_bg = make_color(esc(47), BG_END)

HL_END = esc(22, 27, 39)
#HL_END = esc(22, 27, 0)

black_hl = make_color(esc(1, 30, 7), HL_END)
red_hl = make_color(esc(1, 31, 7), HL_END)
green_hl = make_color(esc(1, 32, 7), HL_END)
yellow_hl = make_color(esc(1, 33, 7), HL_END)
blue_hl = make_color(esc(1, 34, 7), HL_END)
magenta_hl = make_color(esc(1, 35, 7), HL_END)
cyan_hl = make_color(esc(1, 36, 7), HL_END)
white_hl = make_color(esc(1, 37, 7), HL_END)

bold = make_color(esc(1), esc(22))
italic = make_color(esc(3), esc(23))
underline = make_color(esc(4), esc(24))
strike = make_color(esc(9), esc(29))
blink = make_color(esc(5), esc(25))
