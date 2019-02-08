#
#	Nick Quinn - Compiler Construction
#

# R0:
# e ::= number | (read) | (-e) | (+ee)
# p ::= (program any e)

# Class Definitions
# -- Base Class for Expressions --
class expr:
	def interp(self):
		return 0;
# -- Inherited Class for Number Values --
class num(expr):
	def __init__(self, num):
		self._num = num
	def interp(self):
		return self._num;
# -- Inherited Class for Negating Numbers --
class neg(expr):
	def __init__(self, num):
		self._num = num
	def interp(self):
		return -1 * self._num.interp()
# -- Inherited Class for Adding Numbers --
class add(expr):
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs
	def interp(self):
		return self._lhs.interp() + self._rhs.interp();

# -- Inherited Class for Adding Numbers --
class read(expr):
	def interp(self):
		num = input("Please enter a numerical value: ")
		num = int(num)
		return num;
# -- Inherited Class for the Program "Container" --
class prog(expr):
	def __init__(self, info, e):
		self._info = info
		self._e = e
	def interp(self):
		return self._e.interp();
