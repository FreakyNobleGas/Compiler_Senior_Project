#
#	Nick Quinn - Compiler Construction
#
#   This file describes and implements the X language.
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

from support import *

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
		file.write("callq %rax") # This might need to be "_read_int"
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
