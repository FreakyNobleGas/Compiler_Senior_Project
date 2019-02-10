#
#	Nick Quinn - Compiler Construction
#
#	This file defines all of the language data types.

# Language R0:
# e ::= number | (read) | (-e) | (+ee)
# p ::= (program any e)
#
# Language R1:
# e ::= ... | var | let var:= e in e
# var ::= variable-not-otherwise-mentioned

# Class Definitions
# -- Base Class for Expressions --
class expr:
	arry_of_reads = []
	random_arry_of_ints = []
	neg_count = 0	
	opt_flag = 0
	opt_index = 0
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
		if expr.neg_count % 2 == 0:
			return self._num;
		else:
			return self._num * -1;

# -- Inherited Class for Negating Numbers --
class neg(expr):
	def __init__(self, num):
		self._num = num
	def interp(self):
		return -1 * self._num.interp();
	def pretty_print(self):
		return "-" + str(self._num.pretty_print());
	def opt(self):
		expr.neg_count += 1
		temp = self._num.opt()
		expr.neg_count -= 1
		return temp;

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
			self._debug_mode = True
		else:
			self._debug_mode = False

	def interp(self, num = 0, debug_mode = False):
		if self._debug_mode:
			return self._num

		if expr.opt_flag:
			self._num = expr.random_arry_of_ints[expr.opt_index]
			expr.opt_index += 1
			return self._num;

		if debug_mode:
			self._num = int(num)
		else:
			num = input("Please enter a numerical value: ")
			self._num = int(num)

		return self._num;

	def pretty_print(self, num = 0, debug_mode = False):
		return "Read(" + str(self._num) + ")";

	def opt(self, num = 0, debug_mode = False):
		if expr.neg_count % 2 == 0:
			expr.arry_of_reads.insert(0, 1)
		else:
			expr.arry_of_reads.insert(0, -1)
		return 0;

# -- Inherited Class for the Program "Container" --
class prog(expr):
	def __init__(self, info, e):
		self._info = info
		self._e = e
	def interp(self):
		expr.opt_index = 0
		result = self._e.interp()
		result = int(result)
		return print(self._e.pretty_print() + " = " + str(result));
	def pretty_print(self):
		return self._e.pretty_print();
	def opt(self):
		expr.arry_of_reads.clear()
		result = self._e.opt()
		expr.neg_count = 0
		generate = num(result)
		for reads in expr.arry_of_reads:
			if (reads == -1):			
				generate = add(neg(read()), generate)
			elif (reads == 1):
				generate = add(read(), generate)
			else:
				print("Something went wrong. Neither 1 or -1")
		expr.arry_of_reads.clear()
		return prog(None, generate);

# -- Inherited Class for the Let -- R0->R1

class let(expr):
	def __init__(self, x, xe, xb):
		self._x = x
		self._xe = xe
		self._xb = xb



