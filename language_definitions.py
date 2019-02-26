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

### Support Classes ###

########################## Node #########################################################
# -- Node Class for Linked List in Env (Enviroment) --

class node():
	def __init__(self, var, num):
		self._var = var
		self._num = num
		self.next = None


### Language Class Definitions ###

########################## Expr #########################################################
# -- Base Class for Expressions --

class expr:
	# Global Variables - I've placed these here because it's easier to find
	arry_of_reads = []
	arry_of_vars = []
	random_arry_of_ints = []

	num_of_vars = 0
	neg_count = 0	
	opt_flag = 0
	opt_index = 0
	def interp(self):
		return 0;
	def pretty_print(self):
		return 0;
	def opt(self):
		return 0;

########################## Num ##########################################################
# -- Inherited Class for Number Values --

class num(expr):
	def __init__(self, num):
		self._num = num

	def interp(self):
		# Check if self._num is an integer just in case this is called
		# like num(var(x)) in the R1 language
		if isinstance(self._num, int):
			return self._num;
		else:
			return self._num.interp();

	def pretty_print(self):
		if isinstance( self._num, int):
			return str(self._num);
		
		return str(self._num.pretty_print());

	# The neg count is a way of "checking parentheses" to tell if the value should
	# be negative or not
	def opt(self):
		if expr.neg_count % 2 == 0:
			return self._num;
		else:
			return self._num * -1;

########################## Neg ##########################################################
# -- Inherited Class for Negating Numbers --

class neg(expr):
	def __init__(self, num):
		self._num = num

	def interp(self):
		return -1 * self._num.interp();

	def pretty_print(self):
		return "-" + str(self._num.pretty_print());

	def opt(self):
		# Increase neg_count if 
		expr.neg_count += 1
		temp = self._num.opt()
		expr.neg_count -= 1
		return temp;


########################## Add ##########################################################
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
		right_opt = self._rhs.opt()
		left_opt = self._lhs.opt()
		
		# Check whether either expression is a let
		if (type(right_opt) is let) or (type(left_opt) is let):
			# Check if either side is a integer
			if isinstance(right_opt, int): 
				right_opt = num(right_opt)

			if isinstance(left_opt, int):
				left_opt = num(left_opt)

			# Check if either side is a zero so it can be removed 
			if (isinstance(right_opt, num) and (right_opt.opt() == 0)):
				return left_opt;

			if (isinstance(left_opt, num) and (left_opt.opt() == 0)):			
				return right_opt;

			return add(right_opt, left_opt);
		else:
			if (isinstance(right_opt, num) and (right_opt.opt() == 0)):
				return left_opt;

			if (isinstance(left_opt, num) and (left_opt.opt() == 0)):
				return right_opt;
			return right_opt + left_opt;

########################## Read #########################################################
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
		# Check whether neg has been called an even or odd amount of times. This
		# is to prevent a triple negative from creating false positive values
		if expr.neg_count % 2 == 0:
			expr.arry_of_reads.insert(0, 1)
		else:
			expr.arry_of_reads.insert(0, -1)
		return 0;

########################## Let ##########################################################
# -- Inherited Class for the Let -- 

class let(expr):
	def __init__(self, x, xe, xb):
		self._x = x
		self._xe = xe
		self._xb = xb

	def pretty_print(self):
		return "Let " + str(self._x) + " = " + str(self._xe.pretty_print()) + " in " + str(self._xb.pretty_print());

	def interp(self):
		prog.map_env.add_var(self._x, self._xe.interp())
		return self._xb.interp()
	
	def opt(self):

		# Begin working on xe
		num_of_reads = len(expr.arry_of_reads)

		# This will always be an integer since read returns 0
		temp_xe = self._xe.opt()
		xe_result = num(temp_xe)
		xe_result_temp = xe_result
		
		# Number of Reads counted after optomizing xe
		xe_diff_of_reads = (len(expr.arry_of_reads) - num_of_reads)

		# For each read, insert a read() into xe_result
		i = 0
		while i < xe_diff_of_reads:
			if (expr.arry_of_reads[i] == -1):
				if (xe_result_temp == xe_result) and (temp_xe == 0):
					xe_result = neg(read())
				else:	
					xe_result = add(neg(read()), xe_result)
			elif (expr.arry_of_reads[i]):
				if (xe_result_temp == xe_result) and (temp_xe == 0):				
					xe_result = read()
				else:
					xe_result = add(read(), xe_result)
			else:
				print("Something went wrong. Neither 1 or -1 in let opt")
			i += 1

		# Delete reads from array since we do not know if they are positive or negative
		i = 0
		while i < xe_diff_of_reads:
			del expr.arry_of_reads[0]
			i += 1
		
		# Add the xe_result to the linked list (enviroment)
		prog.map_env.add_var(self._x, xe_result)

		# Begin working on xb
		num_of_reads = len(expr.arry_of_reads)
		var_count = expr.num_of_vars
		
		# This will always be an int since var returns 0 if the mapping is not an int
		# and read will return 0
		temp_xb = self._xb.opt()
		xb_result = num(temp_xb)
		xb_result_temp = xb_result

		# Number of reads and vars counted after optomizing xb
		xb_diff_of_reads = (len(expr.arry_of_reads) - num_of_reads)
		diff_of_vars = expr.num_of_vars - var_count
		
		# For each read, insert a read() into xb_result
		i = 0
		while i < xb_diff_of_reads:
			if (expr.arry_of_reads[i] == -1):
				if temp_xb == 0:
					xb_result = neg(read())
				else:			
					xb_result = add(neg(read()), xb_result)
			elif (expr.arry_of_reads[i]):
				if temp_xb == 0:
					xb_result = read()
				else:
					xb_result = add(read(), xb_result)
			else:
				print("Something went wrong. Neither 1 or -1 in let opt")
			i += 1
		
		# Delete reads from array
		i = 0
		while i < xb_diff_of_reads:
			del expr.arry_of_reads[0]
			i += 1

		# For each var, insert vars into xb_result. Var can either be a number or an expression with reads		
		i = 0
		while i < diff_of_vars:
			if (expr.arry_of_vars[i][0] == "+"):
				if (xb_result_temp == xb_result) and (temp_xb == 0):
					xb_result = var(expr.arry_of_vars[i][1])
				else:
					xb_result = add(var(expr.arry_of_vars[i][1]), xb_result)
			else:
				if (xb_result_temp == xb_result) and (temp_xb == 0):
					xb_result = neg(var(expr.arry_of_vars[i][1]))
				else:
					xb_result = add(neg(var(expr.arry_of_vars[i][1])), xb_result)
			i += 1
 
		# Delete var from array
		i = 0
		while i < diff_of_vars:
			del expr.arry_of_vars[0]
			expr.num_of_vars -= 1
			i += 1
		if (xe_diff_of_reads == 0) and (xb_diff_of_reads == 0):
			xb_result = xb_result.opt()
			if isinstance(xb_result, int):
				return xb_result
		return let(self._x, xe_result, xb_result);

########################## Env ##########################################################
# -- Inherited Class env (enviroment) --

class env(expr):
	def __init__(self):
		self._head = None

	def find_var(self, var):
		temp = self._head
		while temp != None:
			if (temp._var == var):
				return temp._num;
			temp = temp.next;
		print (" No mapping found. ")
		return None;

	def add_var(self, var, x):
		new_node = node(var, x)
		if (self._head == None):
			self._head = new_node
		else:
			temp = self._head
			new_node.next = temp
			self._head = new_node
		return;

########################## Var ##########################################################
# -- Inherited Class for Var --

class var(expr):
	def __init__(self, var):
		self._var = var

	def pretty_print(self):
		value = prog.map_env.find_var(self._var)
		if (value == None):
			value = self._var

		if isinstance(value, int):
			return str(self._var) + "(" + str(value) + ")";

		return str(self._var) + "(" + str(value.pretty_print()) + ")";

	def interp(self):
		return prog.map_env.find_var(self._var);

	def opt(self):
		value = prog.map_env.find_var(self._var)

		if isinstance(value, num):
			if expr.neg_count % 2 == 0:
				return value.opt();
			else:
				return value.opt() * -1;
		else:
			expr.num_of_vars += 1
			if expr.neg_count % 2 == 0:
				expr.arry_of_vars.insert(0, ("+", self._var))
			else:
				expr.arry_of_vars.insert(0, ("-", self._var))
			return 0;

########################## Prog #########################################################
# -- Inherited Class for the Program "Container" --

class prog(expr):
	# Global variable that holds the linked list that maps var->num
	map_env = env()

	def __init__(self, info, e):
		self._info = info
		self._e = e

	def interp(self):
		# Index is used for optomization tests so that the default test has the same
		# random read values as the optomized test
		expr.opt_index = 0
		# Save the result first so that we can pretty print
		result = self._e.interp()
		result = int(result)
		return print(str(self._e.pretty_print()) + " = " + str(result));

	def pretty_print(self):
		return str(self._e.pretty_print());

	def opt(self):
		expr.arry_of_reads.clear()
		result = self._e.opt()
		expr.neg_count = 0
		generate = num(result)
		# Insert a read into the program based on if the read was intended to be negative or not
		for reads in expr.arry_of_reads:
			if (reads == -1):
				if (isinstance(result, int)) and (result == 0):
					generate = neg(read())
				else:			
					generate = add(neg(read()), generate)
			elif (reads == 1):
				if (isinstance(result, int)) and (result == 0):
					generate = read()
				else:
					generate = add(read(), generate)
			else:
				print("Something went wrong. Neither 1 or -1")

		return prog(None, generate);



