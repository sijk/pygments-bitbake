#!/usr/bin/env python

from bitbake import BitbakeLexer
from pygments.formatters import Terminal256Formatter
from pygments.formatters import RawTokenFormatter
from pygments import highlight
import fileinput
from sys import argv

if '-r' in argv:
    formatter = RawTokenFormatter()
    argv.remove('-r')
else:
    formatter = Terminal256Formatter(style='native')

print highlight(''.join(fileinput.input()), 
                BitbakeLexer(), 
                formatter)

