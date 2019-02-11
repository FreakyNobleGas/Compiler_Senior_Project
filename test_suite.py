#
#	Nick Quinn - Compiler Construction
#
#	This file is the testing suite, and is primarily used to make
#	sure there are no bugs in the compiler and everything is
#	functioning as expected. This file will also contain other function
#	definitions such as generate

# Imports all the data type definitions
from language_definitions import *
import random

# Return a random number
def rand_num():
	return random.randint(0,10);

# Inserts n random numbers into random_arry_of_ints defined in the
# expr class
def generate_arry_of_ints(n):
	i = 0
	expr.random_arry_of_ints.clear()
	while i < n:
		i += 1
		expr.random_arry_of_ints.append(rand_num())
	return;

# Returns a program of n depth
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
		generate = let(

	return prog(None, generate);

# Returns a program that calculates 2^n
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

# Test random programs
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

	print("\n\n------------- Testing Optomizer -------------\n\n")
	
	while i <= 30:
		generate_arry_of_ints(50)
		print("Test " + str(i) + ": Optomizer")
		test = generate_large_program(rand_num())	
		test.interp()	
		opt_test = test.opt()
		opt_test.interp()
		print("\n")
		i += 1

	while i <= 35:
		generate_arry_of_ints(50)
		print("Test " + str(i) + ": Optomizer")
		test = generate_large_program(0)	
		test.interp()	
		opt_test = test.opt()
		opt_test.interp()
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

	print ("Test 37: Answer = 20")
	test = prog(None, let(y, let(y, neg(read(5, True)), add(var(y), var(y))), neg(add(var(y), var(y)))))
	test.interp()
	print("\n")
	
	





