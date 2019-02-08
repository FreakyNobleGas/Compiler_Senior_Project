#
#	Nick Quinn - Compiler Construction
#

from language_definitions import expr, num, neg, add, read, prog

test = prog(None, neg(add(num(17),add(read(),num(42)))))
print(test.interp())

