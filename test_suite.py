#
#	Nick Quinn - Compiler Construction
#
#	This file is the testing suite, and is primarily used to make
#	sure there are no bugs in the compiler and everything is
#	functioning as expected. This file will also contain other function
#	definitions such as generate large program that is exclusively used for
#	testing.

# Imports all the data type definitions
from language_c import *
from language_x import *
from language_r import *
from support import *
import random
import sys

########################## Random Number ################################################
# -- Return a random number --

def rand_num():
	return random.randint(0,10);

########################## Generate Array of Ints #######################################
# -- Inserts n random numbers into random_arry_of_ints defined in the expr class --

def generate_arry_of_ints(n):
	i = 0
	expr.random_arry_of_ints.clear()
	while i < n:
		i += 1
		expr.random_arry_of_ints.append(rand_num())
	return;

########################## Generate Large Program #######################################
# -- Returns a program of n depth --

def generate_large_program(n, language = None):
	i = 1
	if(language == None):
		# Generate a program with a random number of reads
		if(n == 0):
			random = rand_num()
			generate = read()
			while i <= random:
				i += 1
				generate = add(read(), generate)
		else:
			generate = add(num(rand_num()), num(rand_num()))
			while i < n :
				random = rand_num() % 4
				i += 1
				if (random == 0):
					generate = neg(generate)
				elif (random == 1):
					generate = add(generate, num(rand_num()))
				elif (random == 2):
					generate = add(neg(generate), neg(generate))
				elif (random == 3):
					generate = add(generate, generate)
				else:
					print("Something very wrong happened")

	elif(language == "R1"):
		# Unused vars waiting to be used at random
		input_array = ["b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]

		# vars that have been used. "a" is used by default to initialize the first let
		output_array = ["a"]

		# Create a random number of reads and lets
		if( n == 0 ):
			random = rand_num()

			generate = let(output_array[0], add(read(), read()), add(var(output_array[0]), var(output_array[0])))

			i = 1
			while i <= random:
				xe = read()
				random2 = rand_num()
				while i <= random2:
					i += 1
					xe = add(read(), xe)
				generate = let(input_array[i], xe, add(var(input_array[i]), generate))
		# Base case for depth 1
		elif( n == 1 ):
			generate = let(output_array[0], add(num(rand_num()), num(rand_num())), add(var(output_array[0]), var(output_array[0])))

		# Create nested lets to depth n
		else:
			generate = let(output_array[0], add(var(input_array[0]), num(rand_num())), add(var(output_array[0]), var(input_array[0])))

			i = 0
			# Insert lets up to n depth, or the maximum range of the rand_num() function
			while (i < (n - 1)) and (i < 10):
				# Get a used and unused var
				next_var = input_array[i]

				# Append used var to output array
				output_array.append(next_var)

				# Create new let with unused var, and nest previous lets
				if i == (n - 2):
					generate = let(next_var, add(num(rand_num()), num(rand_num())), add(var(next_var), generate))
				else:
					generate = let(next_var, add(var(input_array[i + 1]), num(rand_num())), add(var(next_var), generate))

				i += 1

	return prog(None, generate);

########################## Generate Large Number ########################################
# -- Returns a program that calculates 2^n --

def generate_large_number(n):
	i = 2
	# Base Case: 2^0 = 1
	if(n == 0):
		generate = num(1)
	# Base Case: 2^1 = 2
	elif( n == 1):
		generate = num(2)
	else:
		generate = add(num(2), num(2))
		while( i < n ):
			i += 1
			generate = add(generate, generate)
	return prog(None, generate);

########################## Testing ######################################################
# -- Test random programs --

def testing():

	print("\n\n------------- Testing Interp -------------\n\n")

	print("Test 1: Answer = -64")
	test = prog(None, neg( add( num(17), add(read(5, True), num(42)))))
	test.interp()
	print("\n")

	print("Test 2: Answer =  -3")
	test = prog(None, add( num(5), neg( num(8))))
	test.interp()
	print("\n")

	print("Test 3: Answer =  10")
	test = prog(None, add( neg(num(-5)), neg(num(-5))))
	test.interp()
	print("\n")

	print("Test 4: Answer = -5")
	test = prog(None, neg(neg(num(-5))))
	test.interp()
	print("\n")

	print("Test 5: Answer =  10,000")
	test = prog(None, add(read(5000, True), num(5000)))
	test.interp()
	print("\n")

	print("Test 6: Answer =  12")
	test = prog(None, num(12))
	test.interp()
	print("\n")

	print("Test 7: Answer =  -15")
	test = prog(None, neg( add( num(5), num(10))))
	test.interp()
	print("\n")

	print("Test 8: Answer = 1200")
	test = prog(None, read(1200, True))
	test.interp()
	print("\n")

	print("Test 9: Answer =  95")
	test = prog(None, add( num(45), num(50)))
	test.interp()
	print("\n")

	print("Test 10: Answer =  -150")
	test = prog(None, neg( add(read(50, True), read(100, True))))
	test.interp()
	print("\n")

	print("Test 11: Answer =  500000000")
	test = prog(None, num(500000000))
	test.interp()
	print("\n")

	print("Test 12: Answer =  24")
	test = prog(None, add(read(12, True), read(12, True)))
	test.interp()

	print("\n\n------------- Testing Generate Large Number -------------\n\n")

	print("Test 13: Answer = 2^0 = 1")
	test = generate_large_number(0)
	test.interp()
	print("\n")

	print("Test 14: Answer = 2^1 = 2")
	test = generate_large_number(1)
	test.interp()
	print("\n")

	print("Test 15: Answer = 2^8 = 256")
	test = generate_large_number(8)
	test.interp()

	print("\n\n------------- Testing Generate Large Program -------------\n\n")
	expr.opt_flag = 1
	i = 16
	while i <= 21:
		generate_arry_of_ints(50)
		random_depth = rand_num()
		print("Test " + str(i) + ": Random Depth " + str(random_depth))
		test = generate_large_program(random_depth)
		test.interp()
		print("\n")
		i += 1

	print("\n\n------------- Testing Optimizer -------------\n\n")

	while i <= 30:
		generate_arry_of_ints(50)
		print("Test " + str(i) + ": Optimizer")
		test = generate_large_program(rand_num())
		test.interp()
		opt_test = test.opt()
		opt_test.interp()
		print("\n")
		i += 1

	while i <= 35:
		generate_arry_of_ints(50)
		print("Test " + str(i) + ": Optimizer")
		test1 = generate_large_program(0)
		test = test1
		test.interp()
		opt_test = test1
		test2 = opt_test.opt()
		test2.interp()
		print("\n")
		i += 1
	expr.opt_flag = 0


	print("\n\n------------- Testing R1 Programs -------------\n\n")

	y = "y"
	print ("Test 36: Answer = 5")
	test = prog(None, let(y, num(5), (var(y))))
	test.interp()
	print("\n")

	print ("Test 37: Answer = 20")
	test = prog(None, let(y, add(num(5), num(5)), add(var(y), var(y))))
	test.interp()
	print("\n")

	print ("Test 38: Answer 80")
	test = prog(None, let(y, neg(add(read(5, True), num(75))), neg(var(y))))
	test.interp()
	print("\n")

	print ("Test 39: Answer = -105")
	test = prog(None, let(y, read(105, True), neg(var(y))))
	test.interp()
	print("\n")

	print ("Test 40: Answer = 60")
	test = prog(None, let(y, add(num(5), add(num(10), num(15))), add(var(y), var(y))))
	test.interp()
	print("\n")

	print ("Test 41: Answer = 0")
	test = prog(None, let(y, add(neg(read(5, True)), num(5)), add(var(y), var(y))))
	test.interp()
	print("\n")

	print ("Test 42: Answer = 40")
	test = prog(None, let(y, neg(num(20)), neg(add(var(y), var(y)))))
	test.interp()
	print("\n")

	print ("Test 43: Answer = 0")
	test = prog(None, let(y, read(5, True), add(neg(var(y)), read(5, True))))
	test.interp()
	print("\n")

	print ("Test 44: Answer = 90")
	test = prog(None, let(y, add(neg(num(45)), neg(num(45))), neg(var(y))))
	test.interp()
	print("\n")

	print ("Test 45: Answer = 18000")
	test = prog(None, let(y, add(num(3000), num(3000)), add( var(y), add(var(y), var(y)))))
	test.interp()
	print("\n")

	print ("Test 46: Answer = -18000")
	test = prog(None, let(y, add(num(3000), num(3000)), neg(add( var(y), add(var(y), var(y))))))
	test.interp()
	print("\n")

	print ("Test 47: Answer = -20")
	test = prog(None, let(y, let(y, neg(read(5, True)), add(var(y), var(y))), add(var(y), var(y))))
	test.interp()
	print("\n")

	print ("Test 48: Answer = 20")
	test = prog(None, let(y, let(y, neg(read(5, True)), add(var(y), var(y))), neg(add(var(y), var(y)))))
	test.interp()
	print("\n")

	print("\n\n------------- Testing R1 Generate Programs -------------\n\n")
	expr.opt_flag = 1

	x = "x"
	y = "y"
	print("TESTING.... 21")
	test = prog(None, let(y, num(5), add( var(y), let(x, add(var(y), num(3)), add(var(x), var(x))))))
	test = test.opt()
	test.interp()
	print("NOT TESTING...")

	i = 48
	while i < 55:
		i += 1
		print("Test ", i ,": Random Generate Program")
		test = generate_large_program(rand_num(), language = "R1")
		test.interp()
		print("\n")

	print("\n\n------------- Testing R1 Optimization -------------\n\n")

	expr.opt_flag = 1
	y = "y"
	x = "x"

	print("\n Testing 56")
	test = prog(None, let(y, add(num(5),num(5)), add(var(y), var(y))))
	test = test.opt()
	print("Interp: " )
	test.interp()

	print("\n Testing 57")
	test = prog(None, let(y, add(num(4),num(5)), add(read(), var(y))))
	test = test.opt()
	print("Interp: ")
	test.interp()

	print("\n Testing 58")
	test = prog(None, let(y, add(read(),num(5)), add(var(y), var(y))))
	test = test.opt()
	print("Interp: ")
	test.interp()

	print("\n Testing 59")
	test = prog(None, let(y, add(read(), num(5)), add(var(y), let(x, add(read(), num(7)), add(var(x), var(x))))))
	test = test.opt()
	print("Interp: ")
	test.interp()
	print("\n")

	i = 60
	while i <= 65:
		generate_arry_of_ints(100)
		print("Test " + str(i) + ": Optimizer")
		test = generate_large_program(rand_num(), "R1")
		test.interp()
		opt_test = test.opt()
		opt_test.interp()
		print("\n")
		i += 1

	while i <= 70:
		generate_arry_of_ints(100)
		print("Test " + str(i) + ": Optimizer")
		test = generate_large_program(0, "R1")
		test.interp()
		opt_test = test.opt()
		opt_test.interp()
		print("\n")
		i += 1

	expr.opt_flag = 0

	print("\n\n------------- Testing X0 Programs -------------\n\n")
	# Holds instruction set
	instr = []
	# Holds label -> block function
	label_map = {}

	print("\n Testing 70 - Answer = 42")

	instr = [\
	movq(xnum(10), xreg("rax")),\
	addq(xnum(32), xreg("rax")),\
	retq()]

	label_map = {"main" : instr}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 71 - Answer = 15")

	instr = [\
	movq(xnum(30), xreg("rax")),\
	subq(xnum(15), xreg("rax")),\
	retq()
	]
	label_map = {"main" : instr}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 72 - Answer = 8")
	instr = [\
	movq(xnum(8), xreg("r8")),\
	movq(xreg("r8"), xreg("r9")),\
	movq(xreg("r9"), xreg("rax")),\
	retq()
	]

	label_map = {"main" : instr}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 73 - Answer = -50")
	instr = [\
	movq(xnum(50), xreg("r10")),\
	negq(xreg("r10")),\
	movq(xreg("r10"), xreg("rax")),\
	retq()
	]
	label_map = {"main" : instr}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 74 - Answer = 20")
	instr = [\
	pushq(xnum(20)),\
	movq(xmem("rsp", 0), xreg("rax")),\
	retq()
	]
	label_map = {"main" : instr}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 75 - Answer = 80")
	instr = [\
	pushq(xnum(20)),\
	pushq(xnum(80)),\
	popq(xreg("rax")),\
	retq()
	]
	label_map = {"main" : instr}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 76 - Answer = Hello World")
	instr = [\
	pushq(xvar("Hello World")),\
	pushq(xnum(80)),\
	popq(xreg("rax")),\
	popq(xreg("rax")),\
	retq()
	]
	label_map = {"main" : instr}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 77 - Answer = 14")

	instr = [\
	movq(xnum(14), xreg("r10")),\
	jmp("end")
	]

	end = [\
	movq(xreg("r10"), xreg("rax")),\
	retq()
	]

	label_map = {"main" : instr, "end": end}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	instr.clear()
	end.clear()
	label_map.clear()

	print("\n Testing 78 - Answer = 42")

	main = [\
	pushq(xreg("rbp")),\
	movq(xreg("rsp"), xreg("rbp")),\
	subq(xnum(16), xreg("rsp")),\
	jmp("start")
	]

	start = [\
	movq(xnum(10), xmem("rbp", -8)),\
	negq(xmem("rbp", -8)),\
	movq(xmem("rbp", -8), xreg("rax")),\
	addq(xnum(52), xreg("rax")),\
	jmp("conclusion")
	]

	conclusion = [\
	addq(xnum(16), xreg("rsp")),\
	popq(xreg("rbp")),\
	retq()
	]

	label_map = {"main" : main, "start": start, "conclusion": conclusion}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	main.clear()
	start.clear()
	conclusion.clear()
	label_map.clear()


	print("\n Testing 79 - Answer = Callq")

	main = [\
	callq("main"),\
	retq()
	]
	label_map = {"main": main}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	main.clear()


	print("\n Testing 80 - Answer = 30")

	main = [\
	movq(xnum(15), xreg("r10")),\
	movq(xreg("r10"), xreg("r11")),\
	addq(xreg("r10"), xreg("r11")),\
	movq(xreg("r11"), xreg("rax")),\
	retq()
	]
	label_map = {"main" : main}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	main.clear()

	print("\n Testing 81 - Answer = -20")

	main = [\
	pushq(xnum(80)),\
	pushq(xnum(100)),\
	popq(xreg("r10")),\
	popq(xreg("r11")),\
	subq(xreg("r10"), xreg("r11")),\
	movq(xreg("r11"), xreg("rax")),\
	retq()
	]
	label_map = {"main": main}
	test = xprog(None, label_map)
	test.emitter()
	test.interp()
	main.clear()

	testing = addq(xnum(5), xreg("rax"))

	print("\n\n------------- Testing C0 Programs -------------\n\n")
	# Set a few common variables as strings
	x = "x"
	y = "y"
	z = "z"
	# Initialize Label Map (Dictionary)
	label_map = {}
	# Initialize Instruction List
	instr = []
	print("\n Testing 82 - Answer = -3")
	instr = [\
		cstmt(x, cadd( carg(5), cneg( carg(8)))),\
		carg(x)
	]
	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 83 - Answer = 15")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(10)),\
		cstmt(z, cadd(carg(x), carg(y))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 84 - Answer = 10")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(x)),\
		cstmt(z, cadd(carg(x), carg(y))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 85 - Answer = -5")
	instr = [\
		carg(-5)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 86 - Answer = -45")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(50)),\
		cstmt(y, cneg(carg(y))),\
		cstmt(z, cadd(carg(x), carg(y))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 87 - Answer = Read Value")
	instr = [\
		cstmt(x, cread()),\
		carg(x)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 88 - Answer = 25")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(10)),\
		cstmt(z, cadd( carg(y), cadd(carg(x), carg(y)))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 89 - Answer = 10")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(10)),\
		cstmt("a", cadd(carg(x), cneg(carg(y)))),\
		cstmt(z, cadd(carg("a"), cadd(carg(x), carg(y)))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 90 - Answer = 10")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(10)),\
		cstmt(z, cadd(carg(x), carg(x))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 91 - Answer = 5 + Read Value")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, cread()),\
		cstmt(z, cadd(carg(x), carg(y))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 92 - Answer = 30")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(10)),\
		cstmt(z, cadd(carg(x), carg(y))),\
		cstmt(z, cadd(carg(z), cadd(carg(x), carg(y)))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 93 - Answer = 60")
	instr = [\
		cstmt(x, carg(5)),\
		cstmt(y, carg(10)),\
		cstmt(z, cadd(carg(x), carg(y))),\
		cstmt(z, cadd(carg(z), cadd(carg(x), carg(y)))),\
		cstmt(z, cadd(carg(z), carg(z))),\
		carg(z)
	]

	label_map = {"main": instr}
	test = cprog(None, label_map)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n\n------------- Testing Uniquify -------------\n\n")

	print("\n Testing 94 - Answer = 30")
	test = prog(None, let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	test.interp()

	print("\n Testing 95 - Answer = 60")
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	test.interp()

	print("\n Testing 96 - Answer= 80")
	test = prog(None, let(y, num(40), add(var(y), let(x, num(20), add(var(x), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	test.interp()

	print("\n\n------------- Testing RCO -----------------\n\n")

	print("\n Testing 97 - Answer = 10")
	test = prog(None, add(num(5), num(5)))
	test.interp()
	print("Running RCO")
	test = test.rco()
	test.interp()

	print("\n Testing 98 - Answer = 15")
	test = prog(None, add(num(5), add(num(5), num(5))))
	test.interp()
	print("Running RCO")
	test = test.rco()
	test.interp()

	print("\n Testing 99 - Answer = -10")
	test = prog(None, neg(add(num(5), num(5))))
	test.interp()
	print("Running RCO")
	test = test.rco()
	test.interp()

	print("\n Testing 100 - Answer = 5")
	test = prog(None, let(x, num(5), var(x)))
	test.interp()
	print("Running RCO")
	test = test.rco()
	test.interp()

	print("\n Testing 101 - Answer = 13")
	test = prog(None, let(x, num(5), add(var(x), num(8))))
	test.interp()
	print("Running RCO")
	test = test.rco()
	test.interp()

	print("\n Testing 102 - Answer = 15")
	test = prog(None, let(x, num(5), add(var(x), let(y, num(10), var(y)))))
	test.interp()
	print("Running RCO")
	test = test.rco()
	test.interp()

	print("\n Testing 103 - Answer = 25")
	test = prog(None, let(y, num(5), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	test.interp()
	print("Running RCO")
	test = test.rco()
	test.interp()

	print("\n Testing 104 - Answer = 60")
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	test.interp()
	print("Running RC0")
	test = test.rco()
	test.interp()

	print("\n\n------------- Testing ECON -----------------\n\n")

	print("\n Testing 105 - Answer = 10")
	test = prog(None, add(num(5), num(5)))
	test.interp()
	test = test.rco()
	print("Running ECON")
	test = test.econ()
	test.interp()

	print("\n Testing 106 - Answer = 15")
	test = prog(None, add(num(5), add(num(5), num(5))))
	test.interp()
	test = test.rco()
	print("Running ECON")
	test = test.econ()
	test.interp()

	print("\n Testing 107 - Answer = 13")
	test = prog(None, let(x, num(5), add(var(x), num(8))))
	test.interp()
	test = test.rco()
	print("Running ECON")
	test = test.econ()
	test.interp()

	print("\n Testing 108 - Answer = 15")
	test = prog(None, let(x, num(5), add(var(x), let(y, num(10), var(y)))))
	test.interp()
	test = test.rco()
	print("Running ECON")
	test = test.econ()
	test.interp()

	print("\n Testing 109 - Answer = 25")
	test = prog(None, let(y, num(5), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	test.interp()
	test = test.rco()
	print("Running ECON")
	test = test.econ()
	test.interp()

	print("\n Testing 110 - Answer = 60")
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	test.interp()
	test = test.rco()
	print("Running ECON")
	test = test.econ()
	test.interp()

	print("\n\n------------- Testing Uncover-Locals -----------------\n\n")

	print("\n Testing 111 - Answer = _u - _u2")
	test = prog(None, add(num(5), num(5)))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	print("\nInterp C0 #2: ")
	test.interp()
	print("Uncover-Locals")
	test = test.uncover()
	print("\nInterp C0 # 3: ")
	test.interp()

	print("\n Testing 112 - Answer = x, _u - u3")
	test = prog(None, let(x, num(5), add(var(x), num(8))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	print("\nInterp C0 #2: ")
	test.interp()
	print("Uncover-Locals")
	test = test.uncover()
	print("\nInterp C0 # 3: ")
	test.interp()

	print("\n Testing 113 - Answer = y, y1, _u - u8 ")
	test = prog(None, let(y, num(5), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	print("\nInterp C0 #2: ")
	test.interp()
	print("Uncover-Locals")
	test = test.uncover()
	print("\nInterp C0 # 3: ")
	test.interp()

	print("\n\n------------- Testing Select -----------------\n\n")

	print("\n Testing 114 - Answer = 10")
	test = prog(None, add(num(5), num(5)))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 115 - Answer = 15")
	test = prog(None, add(num(5), add(num(5), num(5))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 116 - Answer = 13")
	test = prog(None, let(x, num(5), add(var(x), num(8))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 117 - Answer = 15")
	test = prog(None, let(x, num(5), add(var(x), let(y, num(10), var(y)))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 118 - Answer = 25")
	test = prog(None, let(y, num(5), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 119 - Answer = 60")
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n\n------------- Testing Assign Homes -----------------\n\n")

	print("\n Testing 120 - Answer = 10")
	test = prog(None, add(num(5), num(5)))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 121 - Answer = 15")
	test = prog(None, add(num(5), add(num(5), num(5))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 122 - Answer = 13")
	test = prog(None, let(x, num(5), add(var(x), num(8))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 123 - Answer = 15")
	test = prog(None, let(x, num(5), add(var(x), let(y, num(10), var(y)))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 124 - Answer = 25")
	test = prog(None, let(y, num(5), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 125 - Answer = 60")
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()


	print("\n\n------------- Testing Patch -----------------\n\n")

	print("\n Testing 126 - Answer = 10")
	test = prog(None, add(num(5), num(5)))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	test = test.patch()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 127 - Answer = 15")
	test = prog(None, add(num(5), add(num(5), num(5))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	test = test.patch()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 128 - Answer = 13")
	test = prog(None, let(x, num(5), add(var(x), num(8))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	test = test.patch()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 129 - Answer = 15")
	test = prog(None, let(x, num(5), add(var(x), let(y, num(10), var(y)))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	test = test.patch()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 130 - Answer = 25")
	test = prog(None, let(y, num(5), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	test = test.patch()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 131 - Answer = 60")
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.assign_registers()
	test = test.patch()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()


	print("\n\n------------- Testing Main Generation -----------------\n\n")

	print("\n Testing 132 - Answer = 10")
	test = prog(None, add(num(5), num(5)))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph()
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()


	print("\n Testing 133 - Answer = 15")
	test = prog(None, add(num(5), add(num(5), num(5))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph()
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 134 - Answer = 13")
	test = prog(None, let(x, num(5), add(var(x), num(8))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph()
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 135 - Answer = 15")
	test = prog(None, let(x, num(5), add(var(x), let(y, num(10), var(y)))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph()
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 136 - Answer = 25")
	test = prog(None, let(y, num(5), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph()
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n Testing 137 - Answer = 60")
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph()
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n\n------------- Testing Liveness-Analysis -----------------\n\n")
	# Initialize Label Map (Dictionary) & Instruct List
	label_map = {}
	instr = []
	print("\n Testing 138 - Answer = 13")
	print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 139 - Answer = 33")
	print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	print("        6. c ::  7. c :: 8. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		movq(xnum(20), xvar("c")),\
		addq(xreg("rax"), xvar("c")),\
		movq(xvar("c"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 140 - Answer = 5")
	print("ANSWER: 1. None :: 2. None :: 3. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 141 - Answer = 15")
	print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	instr = [\
		movq(xnum(10), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 142 - Answer = 40")
	print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	instr = [\
		movq(xnum(20), xvar("a")),\
		addq(xnum(20), xvar("a")),
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 143 - Answer = 20")
	print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. a,b :: 5. a :: 6. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(10), xvar("b")),\
		addq(xvar("a"), xvar("b")),\
		addq(xvar("b"), xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 144 - Answer = 5")
	print("ANSWER: 1. a :: 2. a :: 3. a :: 4. a :: 5. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		movq(xvar("a"), xvar("c")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 145 - Answer = -5")
	print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		negq(xvar("a")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 146 - Answer = -13")
	print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None :: 6. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		negq(xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 147 - Answer = -20")
	print("ANSWER: 1. a :: 2. a :: 3. b :: 4. b 5. None")
	instr = [\
		movq(xnum(20), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		negq(xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 148 - Answer = 50")
	print("ANSWER 1. None 2. None")
	instr = [\
		movq(xnum(50), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 149 - Answer = 15")
	print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(20), xvar("b")),\
		subq(xvar("a"), xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 150 - Answer = -4")
	print("ANSWER: 1. None :: 2. None :: 3. None :: 4. a :: 5. a :: 6. None")
	instr = [\
		pushq(xnum(4)),\
		popq(xreg("rax")),\
		movq(xreg("rax"), xvar("a")),\
		negq(xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n\n------------- Testing Build-Interference -----------------\n\n")
	# Initialize Label Map (Dictionary) & Instruct List
	label_map = {}
	instr = []
	print("\n Testing 151 - Answer = 13")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	print("ANSWER: a->b,rax :: b->rax")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 152 - Answer = 33")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	#print("        6. c ::  7. c :: 8. None")
	print("ANSWER: a->b,rax :: b->rax ")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		movq(xnum(20), xvar("c")),\
		addq(xreg("rax"), xvar("c")),\
		movq(xvar("c"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 153 - Answer = 5")
	#print("ANSWER: 1. None :: 2. None :: 3. None")
	print("ANSWER: No interference")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 154 - Answer = 15")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	print("ANSWER: a->rax")
	instr = [\
		movq(xnum(10), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 155 - Answer = 40")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	print("ANSWER: No interference")
	instr = [\
		movq(xnum(20), xvar("a")),\
		addq(xnum(20), xvar("a")),
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 156 - Answer = 20")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. a,b :: 5. a :: 6. None")
	print("ANSWER: a->b :: b->a")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(10), xvar("b")),\
		addq(xvar("a"), xvar("b")),\
		addq(xvar("b"), xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 157 - Answer = 5")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. a :: 5. None")
	print("ANSWER: No interference")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		movq(xvar("a"), xvar("c")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 158 - Answer = -5")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	print("ANSWER: a->rax")
	instr = [\
		movq(xnum(5), xvar("a")),\
		negq(xvar("a")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 159 - Answer = -13")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None :: 6. None")
	print("ANSWER: a->b, rax :: b->rax")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		negq(xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 160 - Answer = -20")
	#print("ANSWER: 1. a :: 2. a :: 3. b :: 4. None")
	print("ANSWER: No interference")
	instr = [\
		movq(xnum(20), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		negq(xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 161 - Answer = 50")
	print("ANSWER: No interference")
	instr = [\
		movq(xnum(50), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 162 - Answer = 15")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	print("ANSWER: a->b")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(20), xvar("b")),\
		subq(xvar("a"), xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 163 - Answer = -4")
	#print("ANSWER: 1. None :: 2. None :: 3. None :: 4. a :: 5. a :: 6. None")
	print("ANSWER: No interference")
	instr = [\
		pushq(xnum(4)),\
		popq(xreg("rax")),\
		movq(xreg("rax"), xvar("a")),\
		negq(xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n\n------------- Testing Color Graph -----------------\n\n")
	# Initialize Label Map (Dictionary) & Instruct List
	label_map = {}
	instr = []
	print("\n Testing 164 - Answer = 13")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	#print("ANSWER: a->b,rax :: b->rax")
	print("ANSWER: b:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 165 - Answer = 33")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	#print("        6. c ::  7. c :: 8. None")
	#print("ANSWER: a->b,rax :: b->rax ")
	print("ANSWER: b:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		movq(xnum(20), xvar("c")),\
		addq(xreg("rax"), xvar("c")),\
		movq(xvar("c"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 166 - Answer = 5")
	#print("ANSWER: 1. None :: 2. None :: 3. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 167 - Answer = 15")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	#print("ANSWER: a->rax")
	print("ANSWER: None")
	instr = [\
		movq(xnum(10), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 168 - Answer = 40")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(20), xvar("a")),\
		addq(xnum(20), xvar("a")),
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 169 - Answer = 20")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. a,b :: 5. a :: 6. None")
	#print("ANSWER: a->b :: b->a")
	print("ANSWER: a:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(10), xvar("b")),\
		addq(xvar("a"), xvar("b")),\
		addq(xvar("b"), xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 170 - Answer = 5")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. a :: 5. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		movq(xvar("a"), xvar("c")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 171 - Answer = -5")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	#print("ANSWER: a->rax")
	print("ANSWER: None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		negq(xvar("a")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 172 - Answer = -13")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None :: 6. None")
	#print("ANSWER: a->b, rax :: b->rax")
	print("ANSWER: b:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		negq(xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 173 - Answer = -20")
	#print("ANSWER: 1. a :: 2. a :: 3. b :: 4. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(20), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		negq(xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 174 - Answer = 50")
	#print("ANSWER: 1. None :: 2. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(50), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 175 - Answer = 15")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	#print("ANSWER: a->b")
	print("ANSWER: None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(20), xvar("b")),\
		subq(xvar("a"), xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 176 - Answer = -4")
	#print("ANSWER: 1. None :: 2. None :: 3. None :: 4. a :: 5. a :: 6. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		pushq(xnum(4)),\
		popq(xreg("rax")),\
		movq(xreg("rax"), xvar("a")),\
		negq(xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	# This test is the one we used in class. The answers can be referenced on pdf 5 & 6
	print("\n Testing 177 - Answer = 42")
	print("ANSWER: v:1 t:0 z:1 y:2 x:1")
	instr = [\
		movq(xnum(1), xvar("v")),\
		movq(xnum(46), xvar("w")),\
		movq(xvar("v"), xvar("x")),\
		addq(xnum(7), xvar("x")),\
		movq(xvar("x"), xvar("y")),\
		addq(xnum(4), xvar("y")),\
		movq(xvar("x"), xvar("z")),\
		addq(xvar("w"), xvar("z")),\
		movq(xvar("y"), xvar("t")),\
		negq(xvar("t")),\
		movq(xvar("z"), xreg("rax")),\
		addq(xvar("t"), xreg("rax")),\
		retq()
	]

	label_map = {"main": instr}
	test = xprog(None, label_map)
	print("LIVE ANSWER: ")
	test = test.live_analysis(True)
	print("BUILD INTERFERENCE ANSWER: ")
	test = test.build_interference(True)
	print("COLOR GRAPH ANSWER: ")
	test = test.color_graph(True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n\n------------- Testing Assign Registers -----------------\n\n")
	# Initialize Label Map (Dictionary) & Instruct List
	label_map = {}
	instr = []

	i = 178
	while i != 190:
		generate_arry_of_ints(50)
		# Make random depth anything but 0, so reads don't pop up
		random_depth = rand_num()
		while random_depth == 0:
			random_depth = rand_num()
		print("\nTesting " + str(i))
		test = generate_large_program(random_depth, "R1")
		print("Interp R # 1: ")
		test.interp()
		test = test.rco()
		test = test.econ()
		test = test.uncover()
		test = test.select()
		test = test.live_analysis()
		test = test.build_interference()
		test = test.color_graph()
		test = test.assign_registers()
		test = test.patch()
		test = test.main_gen()
		print("Interp X # 2: ")
		test.interp()
		test.emitter()
		i += 1

	print("\n Testing 190 - Answer = 13")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	#print("ANSWER: a->b,rax :: b->rax")
	print("ANSWER: a:1 b:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0, "b":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 191 - Answer = 33")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	#print("        6. c ::  7. c :: 8. None")
	#print("ANSWER: a->b,rax :: b->rax ")
	print("ANSWER: a:1 b:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		movq(xnum(20), xvar("c")),\
		addq(xreg("rax"), xvar("c")),\
		movq(xvar("c"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0, "b":0, "c":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 192 - Answer = 5")
	#print("ANSWER: 1. None :: 2. None :: 3. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 193 - Answer = 15")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	#print("ANSWER: a->rax")
	print("ANSWER: a:1")
	instr = [\
		movq(xnum(10), xvar("a")),\
		movq(xnum(5), xreg("rax")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 194 - Answer = 40")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(20), xvar("a")),\
		addq(xnum(20), xvar("a")),
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 195 - Answer = 20")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. a,b :: 5. a :: 6. None")
	#print("ANSWER: a->b :: b->a")
	print("ANSWER: a:0 b:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(10), xvar("b")),\
		addq(xvar("a"), xvar("b")),\
		addq(xvar("b"), xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0, "b":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 196 - Answer = 5")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. a :: 5. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		movq(xvar("a"), xvar("c")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0, "b":0, "c":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 197 - Answer = -5")
	#print("ANSWER: 1. a :: 2. a :: 3. a :: 4. None")
	#print("ANSWER: a->rax")
	print("a:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		negq(xvar("a")),\
		addq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 198 - Answer = -13")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None :: 6. None")
	#print("ANSWER: a->b, rax :: b->rax")
	print("ANSWER: a:1 b:1")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(8), xvar("b")),\
		addq(xvar("a"), xreg("rax")),\
		addq(xvar("b"), xreg("rax")),\
		negq(xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0, "b":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 199 - Answer = -20")
	#print("ANSWER: 1. a :: 2. a :: 3. b :: 4. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(20), xvar("a")),\
		movq(xvar("a"), xvar("b")),\
		negq(xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0, "b":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 200 - Answer = 50")
	#print("ANSWER: 1. None :: 2. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		movq(xnum(50), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 201 - Answer = 15")
	#print("ANSWER: 1. a :: 2. a :: 3. a,b :: 4. b :: 5. None")
	#print("ANSWER: a->b")
	print("ANSWER: a:0")
	instr = [\
		movq(xnum(5), xvar("a")),\
		movq(xnum(20), xvar("b")),\
		subq(xvar("a"), xvar("b")),\
		movq(xvar("b"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0, "b":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 202 - Answer = -4")
	#print("ANSWER: 1. None :: 2. None :: 3. None :: 4. a :: 5. a :: 6. None")
	#print("ANSWER: No interference")
	print("ANSWER: None")
	instr = [\
		pushq(xnum(4)),\
		popq(xreg("rax")),\
		movq(xreg("rax"), xvar("a")),\
		negq(xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	uncover_dict = {"a":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	test = test.live_analysis()
	test = test.build_interference()
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	# This test is the one we used in class. The answers can be referenced on pdf 5 & 6
	print("\n Testing 203 - Answer = 42")

	instr = [\
		movq(xnum(1), xvar("v")),\
		movq(xnum(46), xvar("w")),\
		movq(xvar("v"), xvar("x")),\
		addq(xnum(7), xvar("x")),\
		movq(xvar("x"), xvar("y")),\
		addq(xnum(4), xvar("y")),\
		movq(xvar("x"), xvar("z")),\
		addq(xvar("w"), xvar("z")),\
		movq(xvar("y"), xvar("t")),\
		negq(xvar("t")),\
		movq(xvar("z"), xreg("rax")),\
		addq(xvar("t"), xreg("rax")),\
		retq()
	]

	label_map = {"main": instr}
	uncover_dict = {"v":0, "w":0, "x":0, "y":0, "z":0, "t":0}
	test_dict = {"uncover": uncover_dict}
	test = xprog(test_dict, label_map)
	print("X INTERP: ", end = " ")
	test.interp()
	print("LIVE ANSWER: ")
	test = test.live_analysis(True)
	print("BUILD INTERFERENCE ANSWER: ")
	test = test.build_interference(True)
	print("COLOR GRAPH ANSWER: ")
	test = test.color_graph(True)
	test = test.assign_registers()
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n\n------------- Testing Move Biasing -----------------\n\n")
	# Initialize Label Map (Dictionary) & Instruct List
	label_map = {}
	instr = []

	print("\n Testing 204 - Answer = 42")
	#print("ANSWER: v -> w :: w -> x, y, z :: x -> y :: y -> z :: z -> t_1 :: t_1 -> rax")
	print("ANSWER: v:1  t_1:0 z:1 y:2 x:0 ") # X will be 1 without move biasing
	# Problem from the book, this one is used repeatingly through the text in
	# register allocation
	instr = [\
		movq (xnum(1), xvar("v")),\
		movq (xnum(46), xvar("w")),\
		movq (xvar("v"), xvar("x")),\
		addq (xnum(7), xvar("x")),\
		movq (xvar("x"), xvar("y")),\
		addq (xnum(4), xvar("y")),\
		movq (xvar("x"), xvar("z")),\
		addq (xvar("w"), xvar("z")),\
		movq (xvar("y"), xvar("t_1")),\
		negq (xvar("t_1")),\
		movq (xvar( "z"), xreg("rax")),\
		addq (xvar("t_1"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test = test.color_graph(True, True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 205 - Answer = 80")
	print("ANSWER: a -> b,c,d :: b -> c, b :: c -> d")
	instr = [\
		movq(xnum(20), xvar("a")),\
		movq(xnum(40), xvar("b")),\
		movq(xnum(80), xvar("c")),\
		movq(xnum(160), xvar("d")),\
		movq(xvar("a"), xvar("d")),\
		movq(xvar("b"), xvar("d")),\
		movq(xvar("c"), xvar("d")),\
		movq(xvar("d"), xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test = test.color_graph(True, True)
	test.interp()
	instr.clear()
	label_map.clear()

	print("\n Testing 206 - Answer = -300")
	print("ANSWER: a -> b,c,d :: b -> c,d :: c -> d")
	instr = [\
		movq(xnum(20), xvar("a")),\
		movq(xnum(40), xvar("b")),\
		movq(xnum(80), xvar("c")),\
		movq(xnum(160), xvar("d")),\
		addq(xvar("a"), xvar("b")),\
		addq(xvar("b"), xvar("c")),\
		addq(xvar("c"), xvar("d")),\
		movq(xvar("d"), xvar("a")),\
		movq(xvar("a"), xreg("rax")),\
		negq(xreg("rax")),\
		retq()
	]
	label_map = {"main": instr}
	test = xprog(None, label_map)
	test = test.live_analysis()
	test = test.build_interference(True)
	test = test.color_graph(True, True)
	test.interp()
	instr.clear()
	label_map.clear()


	print("\n Testing 207 - Answer = 60")
	print("This is a very long answer")
	# This R language program will generate enough moves to make move baising useful
	test = prog(None, let(y, num(30), add(var(y), let(y, num(10), add( var(y), let(y, add(num(5),num(5)), add(var(y), var(y))))))))
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference(True)
	test = test.color_graph(True, True)
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	test.interp()
	test.emitter()
	instr.clear()
	label_map.clear()

	print("\n Testing 208 - Answer = Random Function")
	test = generate_large_program(7, "R1")
	print("Interp R # 1: ")
	test.interp()
	test = test.rco()
	test = test.econ()
	test = test.uncover()
	test = test.select()
	test = test.live_analysis()
	test = test.build_interference(True)
	test = test.color_graph(True, True)
	test = test.assign_registers()
	test = test.patch()
	test = test.main_gen()
	print("Interp X # 2: ")
	test.interp()
	test.emitter()

	print("\n\n------------- Testing R2 Language -----------------\n\n")

	print("\n Testing 209 - Answer = true")
	test = prog(None, true())
	test.interp()
	print("\n")

	print("\n Testing 210 - Answer = false")
	test = prog(None, false())
	test.interp()
	print("\n")

	print("\n Testing 211 - Answer = 7")
	test = prog(None, sub(num(20), num(13)))
	test.interp()
	print("\n")

	print("\n Testing 212 - Answer = true")
	test = prog(None, rand(true(), true()))
	test.interp()
	print("\n")

	print("\n Testing 213 - Answer = true")
	test = prog(None, ror(false(), true()))
	test.interp()
	print("\n")

	print("\n Testing 214 - Answer = false")
	test = prog(None, rnot(true()))
	test.interp()
	print("\n")

	print("\n Testing 215 - Answer = true")
	test = prog(None, cmp(num(5), "<", num(10)))
	test.interp()
	print("\n")

	print("\n Testing 216 - Answer = 8")
	test = prog(None, rif(cmp(num(8), "==", num(2)), num(4), num(8)))
	test.interp()
	print("\n")

	print("\n Testing 217 - Answer = true")
	test = prog(None, let("x", num(5), cmp(var("x"), ">=", num(1))))
	test.interp()
	print("\n")

	print("\n Testing 218 - Answer = false")
	test = prog(None, rnot(let("y", false(), rnot(var("y")))))
	test.interp()
	print("\n")

	print("\n Testing 219 - Answer = 2")
	test = prog(None, sub(num(5), sub(num(10), num(7))))
	test.interp()
	print("\n")

	print("\n Testing 220 - Answer = 20")
	test = prog(None, let("z", num(5), sub(add(num(10), num(15)), var("z"))))
	test.interp()
	print("\n")

	print("\n\n------------- Testing R2 Type Checker -----------------\n\n")

	print("\n Testing 221 - Answer = FAILED")
	test = prog(None, add(false(), num(5)))
	test.interp()
	print("\n")

	print("\n Testing 222 - Answer = FAILED")
	test = prog(None, sub(num(15), true()))
	test.interp()
	print("\n")

	print("\n Testing 223 - Answer = FAILED")
	test = prog(None, neg(true()))
	test.interp()
	print("\n")

	print("\n Testing 224 - Answer = FAILED")
	test = prog(None, cmp(num(15), "=<", false()))
	test.interp()
	print("\n")

	print("\n Testing 225 - Answer = FAILED")
	test = prog(None, cmp(let("x", false(), x), "<", true()))
	test.interp()
	print("\n")

	print("\n Testing 226 - Answer = FAILED")
	test = prog(None, rnot(num(18)))
	test.interp()
	print("\n")

	print("\n Testing 227 - Answer = FAILED")
	test = prog(None, rif(true(), num(15), false()))
	test.interp()
	print("\n")

	print("\n Testing 228 - Answer = FAILED")
	test = prog(None, rif(num(15), num(15), num(15)))
	test.interp()
	print("\n")

	print("\n Testing 229 - Answer = FAILED")
	test = prog(None, let("y", false(), add(true(), num(10))))
	test.interp()
	print("\n")

	print("\n Testing 230 - Answer = FAILED")
	test = prog(None, let("y", num(5), false()))
	test.interp()
	print("\n")
