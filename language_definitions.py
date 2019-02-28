#
#	Nick Quinn - Compiler Construction
#
#	This file defines all of the language data types.

# Language R0:
#
# e ::= number | (read) | (-e) | (+ee)
# p ::= (program any e)
#
# Language R1:
#
# e ::= ... | var | let var:= e in e
# var ::= variable-not-otherwise-mentioned
#
# Language X0:
#
# Program := program info [label -> block]
# block := block info instr ...
# instr := addq arg1, arg2 | subq arg1, arg2 | movq arg1, arg2
#          retq            | negq arg1       | callq label
#          jmp label       | pushq arg1      | popq arg
# arg :=   number($n)      | reg (%rn)       | mem %rn(offset)
#          var (x)

### Support Classes ###

########################## Node #########################################################
# -- Node Class for Linked List in Env (Enviroment) --

class node():
	def __init__(self, var, num):
		self._var = var
		self._num = num
		self.next = None

########################## Machine State Data Structure #################################

class ms():
	# ms := (reg -> num) x (addr_num -> num) x (var -> num) x (lab -> block)
	# ms0 := (reg = 0) x (addr_num = 0) x (var = 0) x (lab -> block)
	def __init__(self, reg, reg_num, addr, addr_num, var, var_num, label_map, label):
		# Registers
		# -- Bad Reg Names: rsp | rbp | rax | rbx | rcx | rdx | rsi | rdi
		# -- Good Reg Names: reg 8 -> reg 15
		self._reg = reg
		self._reg_num = reg_num
		self._reg_map = {"R8":0, "R9":0, "R10":0, "R11":0, "R12":0, "R13":0, "R14":0, "R15":0, "rsp":0,\
		"rbp":0, "rax":0, "rbx":0, "rcx":0, "rdx":0, "rsi":0, "rdi":0 }
		#self._rsp = []
		#self._rsp_offset = 0
		#self._rbp = []
		#self._rax = []
		#self._rbx = []
		#self._rcx = []
		#self._rdx = []
		#self._rsi = []
		#self._rdi = []

		# Addresses
		self._addr = addr
		self._addr_num = addr_num
		self._addr_map = {0:0}

		# Variables
		self._var = var
		self._var_num = var_num
		self._var_map = {var: var_num}

		# Label Mapping
		# (lab -> block) lets program look up existing labels
		self._label = label
		if label_map == None:
			self._block = None
		else:
			self._block = label_map[label]

	def find(x):
		# If x is a good register
		if (x == "R8") and (x == "R9") and (x == "R10") and (x == "R11") and (x == "R12") and (x == "R13") and (x == "R14") and (x == "R15"):
			return self._reg_map(x);

		# If x is a bad register
		elif(x == "rsp" and x == "rbp" and (x == "rax") and (x == "rbx") and (x == "rcx") and (x == "rdx") and (x == "rsi") and (x == "rdi")):
			print("Need to flesh these registers out\n")
			return self._reg_map(x);

		# If x is a addr
		elif(isinstance(x, int)): # Should make this an arg data type
			return self._addr_map(x);

		# If x is a var
		else: # Should check if this a var data type
			return self._var_map(x);

	def insert(dst, value, offset = 0):

		# If dst is a register
		if (dst == "R8") and (dst == "R9") and (dst == "R10") and (dst == "R11") and (dst == "R12") and (dst == "R13") and (dst == "R14") and (dst == "R15"):
			self._reg_map[dst] = value
			return;

		# If dst is a bad register
		elif((dst == "rbp") and (dst == "rax") and (dst == "rbx") and (dst == "rcx") and (dst == "rdx") and (dst == "rsi") and (dst == "rdi")):
			print("Need to flesh these registers out\n")
			self._reg_map[dst] = value;
			return;

		# If dst is rsp
		elif(dst == "rsp"):

			# For pushq or popq
			# ms[%rsp(0) -> ms(src)]
			self._addr_map[self.reg_map(dst)] = value
			# [%rsp -> ms (%rsp) - 8]
			self._reg_map[dst] = (self.reg_map(dst) + offset)

		# If dst is a addr
		elif(isinstance(dst, int)):
			self._addr_map[dst] = value
			return;

		# If x is a var
		else:
			self._var_map[dst] = value
			return;


### Language Class Definitions ###

########################## X0 Program ###################################################

class xprog:

	# Global var for machine state
	ms = ms(0,0,0,0,0,0, None, "main")

	def __init__(self, info, label_map):
		self._info = info
		# Label will be a hash map (dict) to blocks that hold instructions
		# Label -> Blocks
		self._label_map = label_map

		# Set Label Map for Machine State Zero
		xprog.ms.label_map = label_map

	# Ultimately returns a number
	def interp():

		# Start interp on machine state zero
		 return xblock.interp(self._label);	# Blocks has the ms and label - Where are the instructions?
						     				# Should be ms0 _main | main


########################## Block ########################################################

class xblock:
	def __init__(self, info, instr):
		self._info = info
		# List of instructions
		# Block -> Instructions
		self._instr = instr

	def interp(self, label): # ms x label
		# First instruction should be ms0 and label _main
		return xinstr.interp(xprog.ms._block._instr);

########################## Instruction ##################################################

class xinstr:
	def emitter():
		return 0;

	def interp(self, instr):
		# instr is a list
		# K = What to do next ( But can be pulled from instruction list )
		for i in instr:
			instr[i].interp()

		return;

########################## Addq #########################################################

class addq(xinstr):
	def __init__(self, arg1, arg2):
		self._arg1 = arg1
		self._arg2 = arg2

	def emitter():
		print("addq ", self._arg1.emitter(), " ", self._arg2.emitter())

	def interp(self):
		src = xprog.ms.find(self._arg1.interp())
		result = xprog.ms.find(self._arg2.interp())

		# [ dst -> ms(src) + ms(src)]
		result += src
		xprog.ms.insert(self._arg2, result)

		return;

########################## Subq #########################################################

class subq(xinstr):
	def __init__(self, arg1, arg2):
		self._arg1 = arg1
		self._arg2 = arg2

	def emitter():
		print("subq ", self._arg1.emitter(), " ", self._arg2.emitter())

	def interp(self):
		src = xprog.ms.find(self._arg1.interp())
		result = xprog.ms.find(self._arg2.interp())

		# [ dst -> ms(src) - ms(src)]
		result -= src
		xprog.ms.insert(self._arg2.interp(), result) # Should this be interp?

		return;

########################## Movq #########################################################

class movq(xinstr):
	def __init__(self, arg1, arg2):
		self._arg1 = arg1
		self._arg2 = arg2

	def emitter():
		print("movq ", self._arg1.emitter(), " ", self._arg2.emitter())

	def interp(self):
		src = xprog.ms.find(self._arg1.interp())

		# movq ms' = ms[dst -> ms(src)]
		xprog.ms.insert(self._arg2.interp(), src)

		return;


########################## Retq #########################################################

class retq(xinstr):

	def emitter():
		print("retq")

	def interp():
		# This should be the last instruction
		return xprog.ms.find("rax");

########################## Negq #########################################################

class negq(xinstr):
	def __init__(self, arg):
		self._arg = arg

	def emitter():
		print("negq ", self._arg.emitter())

	def interp(self):
		src = xprog.ms.find(self._arg.interp())
		src *= -1

		xprog.ms.insert(self._arg.interp(), src)

		return;

########################## Callq ########################################################

class callq(xinstr):
	def __init__(self, label):
		self._label = label

	def emitter():
		print("callq ", self._label.emitter())

	# Need to find a way to let the prog know that when it's label hits
	# _read_int, then it needs to come here
	def interp():
		src = input("Please enter a numerical value: ")
		src = int(src)

		xprog.ms.insert("rax", src)
		return;


########################## Jmp ##########################################################

class jmp(xinstr):
	def __init__(self, label):
		self._label = label

	def emitter():
		print("jmp ", self._label.emitter())

	def interp():
		return xblock.interp(self._label);

########################## Pushq ########################################################

class pushq(xinstr):
	def __init__(self, arg):
		self._arg = arg

	def emitter():
		print("pushq ", self._arg.emitter())

	def interp(self):
		xprog.ms.insert("rsp", self._arg.interp(), -8)
		return;

########################## Popq #########################################################

class popq(xinstr):
	def __init__(self, arg):
		self._arg = arg

	def emitter():
		print("popq ", self._arg.emitter())

	def interp(self):
		xprog.ms.insert("rsp", self._arg.interp(), 8)
		return;

########################## Arg ##########################################################

class xarg:
	def emitter():
		return 0;

########################## X0 Number ####################################################

class xnum(xarg):
	def __init__(self, num):
		self._num = num

	def emitter():
		print("$", self._num)

	def interp(self):
		return self._num;

########################## Register #####################################################
# -- Bad Reg Names: rsp | rbp | rax | rbx | rcx | rdx | rsi | rdi
# -- Good Reg Names: reg 8 -> reg 15
class xreg(xarg):
	def __init__(self, reg):
		self._reg = reg

	def emitter():
		print("%", self._reg)

	def interp():
		return self._reg;

########################## Memory #######################################################

class xmem(xarg):
	def __init__(self, offset, reg):
		self._offset = offset
		self._reg = reg

	def emitter():
		print("%", self._reg, "(", self._offset, ")")

	def interp():
		# I'm not sure if this is right, I think this is only used for pointer registers
		return xprog.ms.find(reg) + offset
########################## X0 Var #######################################################

class xvar(xarg):
	def __init__(self, var):
		self._var = var

	def emitter():
		print("(", self._var, ")")

	def interp():
		return self._var;

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

		# Return value if num
		if isinstance(value, num):
			if expr.neg_count % 2 == 0:
				return value.opt();
			else:
				return value.opt() * -1;

		# Otherwise, return the full expression
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
