#
#	Nick Quinn - Compiler Construction
#
#	This file is the testing suite, and is primarily used to make
#	sure there are no bugs in the compiler and everything is
#	functioning as expected. This file will also contain other function
#	definitions such as generate

# Imports all the data type definitions
from language_definitions import expr, num, neg, add, read, prog

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
	
	print("Test 1: Answer = -64")
	test = prog(None, neg( add( num(17), add(read(5, True), num(42)))));
	test.interp()

	print("Test 2: Answer =  -3")
	test = prog(None, add( num(5), neg( num(8))));
	test.interp()

	print("Test 3: Answer =  10")
	test = prog(None, add( neg(num(-5)), neg(num(-5))));
	test.interp()

	print("Test 4: Answer = -5")
	test = prog(None, neg(neg(num(-5))));
	test.interp()

	print("Test 5: Answer =  10,000")
	test = prog(None, add(read(5000, True), num(5000)));
	test.interp()

	print("Test 6: Answer =  12")
	test = prog(None, num(12));
	test.interp()

	print("Test 7: Answer =  -15")
	test = prog(None, neg( add( num(5), num(10))));
	test.interp()

	print("Test 8: Answer = 1200")
	test = prog(None, read(1200, True));
	test.interp()

	print("Test 9: Answer =  95")
	test = prog(None, add( num(45), num(50)));
	test.interp()

	print("Test 10: Answer =  -150")
	test = prog(None, neg( add(read(50, True), read(100, True))));
	test.interp()

	print("Test 11: Answer =  500000000")
	test = prog(None, num(500000000));
	test.interp()

	print("Test 12: Answer =  24")
	test = prog(None, add(read(12, True), read(12, True)));
	test.interp()

	print("Test 13: Answer = 2^0 = 1")
	test = generate_large_number(0)
	test.interp()

	print("Test 14: Answer = 2^1 = 2")
	test = generate_large_number(1)
	test.interp()

	print("Test 15: Answer = 2^8 = 256")
	test = generate_large_number(8)
	test.interp()
