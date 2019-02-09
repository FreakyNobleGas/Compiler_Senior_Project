#
#	Nick Quinn - Compiler Construction
#
#	This file defines all of the language data types.

# Language R0:
# e ::= number | (read) | (-e) | (+ee)
# p ::= (program any e)

# Class Definitions
# -- Base Class for Expressions --
class expr:
	arry_of_reads = []
	neg_flag = 1
	def interp(self):
		return 0;
	def pretty_print(self):
		return 0;
	def opt(self):
		return 0;

# -- Inherited Class for Number Values --
class num(expr):
	def __init__(self, num):
		self._num = num
	def interp(self):
		return self._num;
	def pretty_print(self):
		return str(self._num);
	def opt(self):
		return self._num * expr.neg_flag;

# -- Inherited Class for Negating Numbers --
class neg(expr):
	def __init__(self, num):
		self._num = num
	def interp(self):
		return -1 * self._num.interp();
	def pretty_print(self):
		return "-" + str(self._num.pretty_print());
	def opt(self):
		print("Hitting neg")
		expr.neg_flag *= -1
		return self._num.opt();

# -- Inherited Class for Adding Numbers --
class add(expr):
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs
	def interp(self):
		return self._lhs.interp() + self._rhs.interp();
	def pretty_print(self):
		return "(" + str(self._lhs.pretty_print()) + "+" + str(self._rhs.pretty_print()) + ")";
	def opt(self):
		return self._lhs.opt() + self._rhs.opt();

# -- Inherited Class for Adding Numbers --
class read(expr):
	def __init__(self, num = 0, debug_mode = False):
		if debug_mode:
			self._num = int(num)
		else:
			num = input("Please enter a numerical value: ")
			self._num = int(num)

	def interp(self, num = 0, debug_mode = False):
			return self._num;
	def pretty_print(self, num = 0, debug_mode = False):
		return "Read(" + str(self._num) + ")";
	def opt(self, num = 0, debug_mode = False):
		print("Hitting read")
		expr.arry_of_reads.append(1 * expr.neg_flag)
		return 0;

# -- Inherited Class for the Program "Container" --
class prog(expr):
	def __init__(self, info, e):
		self._info = info
		self._e = e
	def interp(self):
		result = self._e.interp()
		result = int(result)
		return print(self._e.pretty_print() + " = " + str(result));
	def pretty_print(self):
		return self._e.pretty_print();
	def opt(self):
		generate = self._e.opt()
		expr.neg_flag = 1
		generate = num(self._e.opt())
		#print(expr._num_of_reads)
		for reads in expr.arry_of_reads:
			if (reads == -1):
				generate = add(neg(read()), generate)
			elif (reads == 1):
				generate = add(read(), generate)
			else:
				print("Something went wrong. Neither 1 or -1")
		expr.arry_of_reads = []
		return prog(None, generate);






