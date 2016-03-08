#!/bin/python

__author__ = 'donkeyxote'

'''
module for colorful output
'''

colors = {'gray': ('\033[', ';30m'),
          'red': ('\033[', ';31m'),
          'green': ('\033[', ';32m'),
          'yellow': ('\033[', ';33m'),
          'blue': ('\033[', ';34m'),
          'magenta': ('\033[', ';35m'),
          'cyan': ('\033[', ';36m'),
          'white': ('\033[', ';37m'),
          }


def colorprint(*args, **kwargs):
    prefix = None
    suffix = None
    bold = '0'

    if kwargs.__contains__('bold'):
        if kwargs['bold']:
            bold = '1'
        kwargs.pop('bold', '')

    if kwargs.__contains__('col'):
        if colors.__contains__(kwargs['col']):
            color = colors[kwargs['col']]
            prefix = color[0] + bold + color[1]
            suffix = '\033[' + bold + ';m'
        kwargs.pop('col', '')

    if prefix is not None and suffix is not None:
        if len(args) > 1:
            args = (prefix + str(args[0]),) + args[1:len(args) - 1] + (str(args[len(args) - 1]) + suffix,)
        elif len(args) == 1:
            args = (prefix + str(args[0]) + suffix,)

    print(*args, **kwargs)


if __name__ == '__main__':

    for color in colors:
        colorprint(color, col=color)
    for color in colors:
        colorprint(color, col=color, bold=True)
