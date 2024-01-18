# Copyright: 2022, Alexan Mardigian
__author__ = "Alexan Mardigian, Techno-Hwizrdry"

from collections.abc import Iterable
from colored import attr, fg, names, stylize
from colour import Color
from functools import partial
from typing import Generator
import random

def rprint(text: object, seq: int = 0, **kwargs) -> None:
    '''
    Prints text in color pattern, based on the selected sequence (seq).
    This function can also take the same arguments as Python's print()
    via **kwargs.
    '''
    sequences = {
        0: magenta_gradient,
        1: partial(basic_gradient, 
                   kwargs.get('start', ''), 
                   kwargs.get('end', ''))
    }
    color = sequences[seq]()
    colored_chars = []
    chars = text if isinstance(text, Iterable) else str(text)

    for char in chars:
        text_color = next(color)
        style = stylize(char, fg(text_color), attr(0))
        colored_chars.append(style)

    sep   = kwargs.get('sep')
    end   = kwargs.get('end')
    _file = kwargs.get('file')
    flush = kwargs.get('flush')

    print(''.join(colored_chars), sep=sep, end=end, file=_file, flush=flush)

def magenta_gradient() -> Generator[int, None, None]:
    '''
    Generates an integer that corresponds to a color in this gradient.
    '''
    colors = names[19:230]
    index = random.randint(0, len(colors) - 1)

    while True:
        yield colors[index].lower()
        index = (1 + index) % len(colors)

def basic_gradient(start: str='', end: str='') -> Generator[int, None, None]:
    '''
    Generates an integer that corresponds to a color in this gradient.
    A start color and an end color can be specified via the start and
    end parameters.  The default start and end are 'red'
    and 'blue' respectively.
    '''
    _start = Color(start if start else 'red')
    _end = Color(end if end else 'blue')
    colors = list(_start.range_to(_end, 256))
    index  = random.randint(0, len(colors) - 1)

    while True:
        yield colors[index].get_hex()
        index = (1 + index) % len(colors)
        