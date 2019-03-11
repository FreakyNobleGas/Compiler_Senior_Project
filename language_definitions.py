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
#
# Language C0:
#
# p := (program info [label -> tail] ... )
# tail := (return arg) | (seq stmt tail)
# stmt := set var expr
# expr := arg | (read) | (-arg) | (+ arg arg)
# arg := number | var
#


### Support Classes ###

########################## Node #########################################################
# -- Node Class for Linked List in Env (Enviroment) --

class node():
	def __init__(self, var, num):
		self._var = var
		self._num = num
		self.next = None

########################## Env ##########################################################
# -- Class env (enviroment) --

class env():
	def __init__(self):
		self._head = None

	def find_var(self, var):
		temp = self._head
		while temp != None:
			if (temp._var == var):
				return temp._num;
			temp = temp.next;
		#print (" No mapping found. ")
		return None;

	def add_var(self, var, x):
		new_node = node(var, x)
		if (self._head == None):
			self._head = new_node
		else:
			temp = self._head
			new_node.next = temp
			self._head = new_node

########################## Uniquify #####################################################

def uniquify(var, enviroment):
	unique_count = 1
	temp = enviroment.find_var(var)
	new_var = var
	while(temp != None):
		new_var = var + str(unique_count)
		temp = enviroment.find_var(new_var)
		unique_count += 1

	return new_var;

#########################################################################################
##########################        C0 Language           #################################
#########################################################################################

########################## C Program ####################################################
class cprog():
	# Program = (Program Info [label->tail])
	def __init__(self, info, label):
		self._info = info
		self._label = label

	def interp(self):
		# Empty enviroment
		cenv = env()
		instr = self._label["main"]
		return print("return ", ctail.interp(cenv, instr), "\n")

########################## C Tail ########################################################
class ctail():
	# tail = (return arg) | (sequence statement tail)
	def __init__(self, info):
		self._info = info

	def interp(cenv, instr):
		for i in instr:
			if isinstance(i, cstmt):
				# sequence stmt tail
				i.interp(cenv)
			else:
				# Return Arg
				arg = i.interp(cenv)
				return arg;

		return "Error: No return statement."

########################## C Statement ##################################################
class cstmt():
	# Statement = set: var expresion
	def __init__(self, var, expr):
		self._var = var
		self._expr = expr

	def interp(self, cenv):
		# env [x -> (interp expression)]
		expr = self._expr.interp(cenv)
		cenv.add_var(self._var, expr)
		return;

########################## C Expression #################################################
class cexpr():
	# Expression = arg | (read) | (-arg) | (+ arg arg)
	def __init__(self, arg):
		self._arg = arg

	def interp(self, cenv):
		return self._arg.interp(cenv);

########################## C Read #######################################################
class cread():
	def __init__(self):
		pass

	def interp(self, cenv):
		num = input("Please enter a numerical value: ")
		self._num = int(num)
		print(" read ", self._num, " ")
		return self._num;

########################## C Negate #####################################################
class cneg():
	def __init__(self, arg):
		self._arg = arg

	def interp(self, cenv):
		result = self._arg.interp(cenv)
		result *= -1
		print("Neg(", result, ")")
		return result

########################## C Add ########################################################
class cadd():
	def __init__(self, arg1, arg2):
		self._arg1 = arg1
		self._arg2 = arg2

	def interp(self, cenv):
		arg1 = self._arg1.interp(cenv)
		arg2 = self._arg2.interp(cenv)
		result = arg1 + arg2
		print("add(", arg1, ",", arg2, ")")
		return result;

########################## C Argument ###################################################
class carg():
	# arg = number | var
	def __init__(self, arg):
		self._arg = arg

	def interp(self, cenv):
		# If arg is just a number
		if isinstance(self._arg, int):
			return self._arg;
		# If arg is a var
		arg = cenv.find_var(self._arg)
		return arg;

#########################################################################################
##########################        X0 Language           #################################
#########################################################################################

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
		self._reg_map = {"r8":0, "r9":0, "r10":0, "r11":0, "r12":0, "r13":0, "r14":0, "r15":0, "rsp":0,\
		"rbp":0, "rax":0, "rbx":0, "rcx":0, "rdx":0, "rsi":0, "rdi":0 }

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

	def find(self, x):
		# If x is a good register
		if (x == "r8") or (x == "r9") or (x == "r10") or (x == "r11") or (x == "r12") or (x == "r13") or (x == "r14") or (x == "r15"):
			return xprog.ms._reg_map[x];

		# If x is a bad register
		elif((x == "rsp") or (x == "rbp") or (x == "rax") or (x == "rbx") or (x == "rcx") or (x == "rdx") or (x == "rsi") or (x == "rdi")):
			return xprog.ms._reg_map[x];

		# If x is a addr
		elif(isinstance(x, int)): # Should make this an arg data type
			return xprog.ms._addr_map[x];

		# If x is a var ( represented by a string )
		else: # Should check if this a var data type
			return xprog.ms._var_map[x];

	def insert(self, dst, value, offset = 0):

		# If dst is a register
		if (dst == "r8") or (dst == "r9") or (dst == "r10") or (dst == "r11") or (dst == "r12") or (dst == "r13") or (dst == "r14") or (dst == "r15"):
			xprog.ms._reg_map[dst] = value
			return;

		# If dst is a bad register
		elif((dst == "rax") or (dst == "rbx") or (dst == "rcx") or (dst == "rdx") or (dst == "rsi") or (dst == "rdi")):
			xprog.ms._reg_map[dst] = value;
			return;

		elif dst == "rbp":
			# Find current value in rbp
			address = xprog.ms._reg_map[dst]
			# Calculate offset
			address += offset
			# Insert value
			xprog.ms._reg_map[address] = value

		# If dst is rsp
		elif(dst == "rsp"):

			# pushq
			if offset == -8:
				# If value is a register, find the value
				if (value == "r8") or (value == "r9") or (value == "r10") or (value == "r11") or (value == "r12") or (value == "r13") or\
				 (value == "r14") or (value == "r15") or (value == "rsp") or (value == "rbp") or (value == "rax") or (value == "rbx") or\
				 (value == "rcx") or (value == "rdx") or (value == "rsi") or (value == "rdi"):
					value = xprog.ms.find(value)

				# [%rsp -> ms (%rsp) - 8]
				xprog.ms._reg_map[dst] = (xprog.ms._reg_map[dst] + offset) # Increase rsp

				# ms[%rsp(0) -> ms(src)]
				xprog.ms._addr_map[xprog.ms._reg_map[dst]] = value # Update value of current position

			# popq
			elif offset == 8:
				# Insert value from the top of the stack to value passed
				xprog.ms.insert(value, xprog.ms._addr_map[xprog.ms._reg_map[dst]])

				# Decrease rsp
				xprog.ms._reg_map[dst] = (xprog.ms._reg_map[dst] + offset)


		# If dst is a addr
		elif(isinstance(dst, int)):
			xprog.ms._addr_map[dst] = value
			return;

		# If x is a var
		else:
			xprog.ms._var_map[dst] = value
			return;


### Language Class Definitions ###

########################## X0 Program ###################################################

class xprog:

	# Global var for machine state
	ms = ms(0,0,0,0,0,0, None, "main")
	num_of_tests = 0

	def __init__(self, info, label_map):
		self._info = info
		# Label will be a hash map (dict) to blocks that hold instructions
		# Label -> Blocks
		self._label_map = label_map
		xprog.ms = ms(0,0,0,0,0,0, None, "main")

	def emitter(self, var = 0):
		# Open file for writing
		file = open("assembly_tests/test_" + str(xprog.num_of_tests) + ".asm", "w+")
		xprog.num_of_tests += 1

		# Begin program
		file.write("globl .main\n")
		xprog.ms._label_map = self._label_map

		# Call emitter on the rest of instructions
		xblock.emitter(file, "main")

		# Close file
		file.close()

		return;

	# Ultimately returns a number
	def interp(self):
		# Set Label Map for Machine State Zero
		xprog.ms._label_map = self._label_map

		# Start interp on machine state zero
		return xblock.interp("main");	# Blocks has the ms and label - Where are the instructions?
						     				# Should be ms0 _main | main


########################## Block ########################################################

class xblock:
	def __init__(self, info, instr):
		self._info = info
		# List of instructions
		# Block -> Instructions
		self._instr = instr

	def emitter(file, label):
		# Set block to instruction set
		xprog.ms._block = xprog.ms._label_map[label]
		file.write(label + ":\n")
		# xprog.ms._block contains a list of instructions
		xinstr.emitter(file, xprog.ms._block)

		return;

	def interp(label): # ms x label
		# Set block to instruction set
		xprog.ms._block = xprog.ms._label_map[label]

		# First instruction should be ms0 and label _main
		# xprog.ms._block contains a list of instructions
		return xinstr.interp(xprog.ms._block);

########################## Instruction ##################################################

class xinstr:
	def emitter(file, instr):
		# Each i in instr is a instruction (ie - addq(xnum(5), xreg("rax")))
		for i in instr:
			i.emitter(file)
			file.write("\n")

		return;

	def interp(instr):
		# instr is a list
		# K = What to do next ( But can be pulled from instruction list )
		for i in instr:
			i.interp()

		return;

########################## Addq #########################################################

class addq(xinstr):
	def __init__(self, arg1, arg2):
		self._arg1 = arg1
		self._arg2 = arg2

	def emitter(self, file):
		file.write("addq ")
		self._arg1.emitter(file)
		file.write(", ")
		self._arg2.emitter(file)

		return;

	def interp(self):
		src = self._arg1.interp()
		if not isinstance(src, int):
			src = xprog.ms.find(src)

		result = self._arg2.interp()
		if not isinstance(result, int):
			result = xprog.ms.find(result)

		# [ dst -> ms(src) + ms(src)]
		result += src
		xprog.ms.insert(self._arg2.interp(), result)

		return;

########################## Subq #########################################################

class subq(xinstr):
	def __init__(self, arg1, arg2):
		self._arg1 = arg1
		self._arg2 = arg2

	def emitter(self, file):
		file.write("subq ")
		self._arg1.emitter(file)
		file.write(", ")
		self._arg2.emitter(file)

		return;

	def interp(self):
		src = self._arg1.interp()
		if not isinstance(src, int):
			src = xprog.ms.find(src)

		result = self._arg2.interp()
		if not isinstance(result, int):
			result = xprog.ms.find(result)

		# [ dst -> ms(src) + ms(src)]
		result -= src
		xprog.ms.insert(self._arg2.interp(), result)

		return;
########################## Movq #########################################################

class movq(xinstr):
	def __init__(self, arg1, arg2):
		self._arg1 = arg1
		self._arg2 = arg2

	def emitter(self, file):
		file.write("movq ")
		self._arg1.emitter(file)
		file.write(", ")
		self._arg2.emitter(file)
		return;

	def interp(self):
		value = self._arg1.interp()
		destination = self._arg2.interp()
		# movq ms' = ms[dst -> ms(src)]

		if not isinstance(self._arg1, xnum):
			value = xprog.ms.find(value)

		xprog.ms.insert(destination, value)

		return;


########################## Retq #########################################################

class retq(xinstr):

	def __init__(self):
		pass

	def emitter(self, file):
		file.write("retq")
		return;

	def interp(self):
		# This should be the last instruction
		print(xprog.ms.find("rax"))
		return xprog.ms.find("rax");

########################## Negq #########################################################

class negq(xinstr):
	def __init__(self, arg):
		self._arg = arg

	def emitter(self, file):
		file.write("negq ")
		self._arg.emitter(file)
		return;

	def interp(self):
		src = xprog.ms.find(self._arg.interp())
		src *= -1

		xprog.ms.insert(self._arg.interp(), src)

		return;

########################## Callq ########################################################

class callq(xinstr):
	def __init__(self, label):
		self._label = label

	def emitter(self, file):
		# rax is the default label for callq
		file.write("callq %rax")
		return;

	# Need to find a way to let the prog know that when it's label hits
	# _read_int, then it needs to come here
	def interp(self):
		src = input("Please enter a numerical value: ")
		src = int(src)

		xprog.ms.insert("rax", src)
		return;


########################## Jmp ##########################################################

class jmp(xinstr):
	def __init__(self, label):
		self._label = label

	def emitter(self, file):
		file.write("jmp ")
		xblock.emitter(file, self._label)
		return;

	def interp(self):
		return xblock.interp(self._label);

########################## Pushq ########################################################

class pushq(xinstr):
	def __init__(self, arg):
		self._arg = arg

	def emitter(self, file):
		file.write("pushq ")
		self._arg.emitter(file)
		return;

	def interp(self):
		xprog.ms.insert("rsp", self._arg.interp(), -8)
		return;

########################## Popq #########################################################

class popq(xinstr):
	def __init__(self, arg):
		self._arg = arg

	def emitter(self, file):
		file.write("popq ")
		self._arg.emitter(file)
		return;

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

	def emitter(self, file):
		file.write("$" + str(self._num));
		return;

	def interp(self):
		return self._num;

########################## Register #####################################################
# -- Bad Reg Names: rsp | rbp | rax | rbx | rcx | rdx | rsi | rdi
# -- Good Reg Names: reg 8 -> reg 15
class xreg(xarg):
	def __init__(self, reg):
		self._reg = reg

	def emitter(self, file):
		file.write("%" + self._reg)
		return;

	def interp(self):
		return self._reg;

########################## Memory #######################################################

class xmem(xarg):
	def __init__(self, reg, offset):
		self._reg = reg
		self._offset = offset

	def emitter(self, file):
		file.write("%" + self._reg + "(" + str(self._offset) + ")");
		return;

	def interp(self):
		# Look up value from the register
		address = xprog.ms.find(self._reg)

		# Look up value + offset in address mapping in machine state
		address = address + self._offset

		return address;

########################## X0 Var #######################################################

class xvar(xarg):
	def __init__(self, var):
		self._var = var

	def emitter(self, file):
		file.write("(" + self._var + ")")
		return;

	def interp(self):
		return self._var;

#########################################################################################
##########################     R0 & R1 Languages     ####################################
#########################################################################################

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
	def unique(self, unique):
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

	def uniq(self, unique_var):
		return;

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

	def uniq(self, unique_var):
		self._num.uniq(unique_var)
		return;

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

	def uniq(self, unique_var):
		# If either side is a let, then we do not want to go further since
		# we call uniq from let for each instance of a let
		if(type(self._lhs) is not let):
			self._lhs.uniq(unique_var)
		if(type(self._rhs) is not let):
			self._rhs.uniq(unique_var)
		return;

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

	def uniq(self, unique_var):
		return;

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
		# Immediately call Uniquify to avoid duplicate variables in env
		self._x = uniquify(self._x, prog.map_env)
		self._xb.uniq(self._x)

		prog.map_env.add_var(self._x, self._xe.interp())
		return self._xb.interp()

	def opt(self):
		# Immediately call Uniquify to avoid duplicate variables in env
		self._x = uniquify(self._x, prog.map_env)
		self._xb.uniq(self._x)

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

	def uniq(self, unique_var):
		print("Error: uniq let function should not have been hit.")
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

	def uniq(self, unique_var):
		self._var = unique_var
		return;


########################## Prog #########################################################
# -- Inherited Class for the Program "Container" --

class prog(expr):
	# Global variable that holds the linked list that maps var->num
	map_env = env()

	def __init__(self, info, e):
		self._info = info
		self._e = e

	def interp(self):
		# Reinitialize Enviroment Mapping
		prog.map_env = env()

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
		# Reinitialize Enviroment Mapping
		prog.map_env = env()

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

	def uniq(self, unique_var):
		print ("Error: uniq prog function should not have been hit.")
		return;
