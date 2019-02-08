#
#	Nick Quinn - Compiler Construction
#
# 	This file is the main driver for the compiler and imports
#	all the neccessary files to build the compiler.

from language_definitions import expr, num, neg, add, read, prog
from test_suite import *


def main():
	testing()

main()
