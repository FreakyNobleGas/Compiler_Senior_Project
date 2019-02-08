#
#	Nick Quinn - Compiler Construction
#


# R0:
# e ::= number | (read) | (-e) | (+ee)
# p ::= (program any e)

# Class Definitions

class expr:
	def interp(self):
		return 0;

class num(expr):
	def __init__(self, num):
		self._num = num
	def interp(self):
		return self._num;

class neg(expr):
	def __init__(self, num):
		self._num = num
	def interp(self):
		return -1 * self._num.interp()

class add(expr):
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs
	def interp(self):
		return self._lhs.interp() + self._rhs.interp();

class read(expr):
	def interp(self):
		num = input("Please enter a numerical value: ")
		num = int(num)
		return num;

class prog(expr):
	def __init__(self, info, e):
		self._info = info
		self._e = e
	def interp(self):
		return self._e.interp();

test = prog(None, neg(add(num(17),add(read(),num(42)))))
print (test.interp())

