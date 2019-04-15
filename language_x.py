#
#    Nick Quinn - Compiler Construction
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
import os
import subprocess

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
    # Holds all the available registers
    reg_set = ["r8", "r9", "r10", "r11", "r12", "r15"]

    def __init__(self, info, label_map):
        self._info = info
        # Label will be a hash map (dict) to blocks that hold instructions
        # Label -> Blocks
        self._label_map = label_map
        xprog.ms = ms(0,0,0,0,0,0, None, "main")

    def emitter(self, var = 0):

        # Store the original working directory
        cur_path = os.path.dirname(os.path.realpath(__file__))

        # Change directories to create assembly test folder
        os.chdir(cur_path + "/assembly_tests")
        if(os.path.isdir("./test_" + str(xprog.num_of_tests)) is False):
            os.mkdir("./test_" + str(xprog.num_of_tests))

        os.chdir(cur_path + "/assembly_tests/test_" + str(xprog.num_of_tests))
        # Open assembly source code file
        file = open("x.s", "w+")
        file_name = "x.s"
        xprog.num_of_tests += 1

        # Begin program
        file.write(".globl main\n")
        xprog.ms._label_map = self._label_map

        # Call emitter on the rest of instructions
        if( "_main" in xprog.ms._label_map):
            # Go through each label and emit instructions
            xblock.emitter(file, "_main")
            xblock.emitter(file, "begin")

            # Copy runtime.c to assembly file directory
            os.system("cp ../../runtime.c .")

        elif( "begin" in xprog.ms._label_map):
            xblock.emitter(file, "begin")
        else:
            xblock.emitter(file, "main")

        # Close file
        file.close()

        if( "_main" in xprog.ms._label_map):
            # Create assembly binary file for execution
            os.system("cc runtime.c x.s -o x.bin")
            # Run executable
            os.system("./x.bin")

        # Go back to original directory
        os.chdir(cur_path)

        return;

    # Ultimately returns a number
    def interp(self):
        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        # Start interp on machine state zero
        if("_main" in xprog.ms._label_map):
            return xblock.interp("_main");
        elif( "begin" in xprog.ms._label_map):
            return xblock.interp("begin");
        else:
            return xblock.interp("main");

    # Takes an X program and returns a set of all the variables assigned to registers
    def live_analysis(self):
        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        # Holds the sets of all of the variables and their correpsonding registers
        # Register can be r8 through r15
        live_set = {}

        # Holds all the available registers
        xprog.reg_set = ["r8", "r9", "r10", "r11", "r12", "r15"]

        # Perform analysis on main and any other labels jumped to
        live_set = xblock.live_analysis("main", live_set)

        return xprog(live_set, self._label_map);

    # Takes a X prog w/ vars, and returns a xprog w/o vars
    def assign_homes(self):
        # Find number of variables to push to stack and adjust for memory size
        vc = len(self._label_map) * 8

        # Make sure memory size for variables is divisible by 16
        if (vc % 16 != 0):
            vc = (len(self._label_map) + 1) * 8

        # Instructions to start program
        begin_instr =\
        [ pushq(xreg("rbp")),\
        movq(xreg("rsp"), xreg("rbp")),\
        addq(xnum(vc), xreg("rsp")),\
        jmp("next")
        ]
        self._label_map["begin"] = begin_instr

        # ** I changed subq to to addq in begin, and vice versa in end. Not sure if this **
        # ** should be changed **

        # Instructions to end program
        end_instr =\
        [ subq(xnum(vc), xreg("rsp")),\
        popq(xreg("rbp")),\
        retq()
        ]
        self._label_map["end"] = end_instr

        # Contains all variables in program
        all_vars = self._info

        # Create a new enviroment that contains the address of each
        # variable on the stack
        var_env = env()

        # ** Does byte count need to be negative? **
        byte_count = 8
        list_of_vars = []
        for vars in all_vars:
            # Add memory address on the stack for current var
            var_env.add_var(vars, xmem("rsp", byte_count))
            byte_count += 8

        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        xblock.assign_homes("main", var_env)

        # Update instruction block after call to assign homes
        xprog.ms._label_map["main"] = xprog.ms._block

        self._label_map["next"] = self._label_map["main"]
        del self._label_map["main"]

        return xprog(self._info, self._label_map)

    # Make sure memory references are legal
    def patch(self):
        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        xblock.patch()

        return xprog(self._info, self._label_map);

    # Add _main label so programs are actually executable assembly code
    def main_gen(self):

        # Add block for _main instructions
        main_instr = [\
        callq("begin"),\
        movq(xreg("rax"), xreg("rdi")),\
        callq("_print_int"),\
        retq()
        ]

        self._label_map["_main"] = main_instr

        return xprog(self._info, self._label_map);



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

        if(label == "_main"):
            file.write("main:\n")
        else:
            file.write(label + ":\n")

        # xprog.ms._block contains a list of instructions
        xinstr.emitter(file, xprog.ms._block)

        return;

    def interp(label): # ms x label
        # Set block to instruction set
        xprog.ms._block = xprog.ms._label_map[label]

        # Operating system uses "main" for assembly instructions
        if(label == "_main"):
            print("main:")
        else:
            print(label, ":")

        # First instruction should be ms0 and label _main
        # xprog.ms._block contains a list of instructions
        return xinstr.interp(xprog.ms._block);

    def live_analysis(label, live_set):
        xprog.ms._block = xprog.ms._label_map[label]

        # Holds the list of instructions for this block
        live_var = []
        live_var = xinstr.live_analysis(xprog.ms._block, live_var)

        # Assign variables with their registers to this live set block
        live_set[label] = live_var

        for vars in live_var:
            print(vars)

        return live_set;

    def assign_homes(label, var_env):
        # Update instruction block
        xprog.ms._block = xprog.ms._label_map[label]

        xinstr.assign_homes(xprog.ms._block, var_env)
        return;

    def patch():

        # Go through each label and remove illegal memory references
        for labels in xprog.ms._label_map:

            # Update instruction block
            xprog.ms._block = xprog.ms._label_map[labels]

            # Patch will return an updated list of instructions
            xprog.ms._label_map[labels] = xinstr.patch(xprog.ms._block)

        return;
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

    def live_analysis(instr, live_var):
        # Length of instruction set
        index = 0
        # Reverse instruction set
        instr.reverse()

        #live_var = []
        # Holds the previous set of registers and variables
        prev_vars = []

        live_index = 0
        while (index < len(instr)):
            temp = instr[index]
            print("TEMP IS", type(temp))
            print("Live before:", live_var)
            print("Prev before:", prev_vars)
            set_of_vars = temp.live_analysis(prev_vars)
            print("Set:", set_of_vars)
            print("Live after:", live_var)
            print("Prev after:", prev_vars)
            #print("LENGTH OF SET IS ", len(set_of_vars))

            if (set_of_vars == []):
                live_var.append([])
            else:
                print("Before append:", live_var)
                live_var.append(set_of_vars)
                print("After append:", live_var)

            #live_var1.insert(live_index, set_of_vars)
            #print("LENGTH OF LIVE AT INDEX ", live_index, " IS ", len(live_var1[live_index]))
            #print(live_var1[live_index], "PRINTING")
            #print("TYPE OF LIVE IS ", type(live_var1), " TYPE OF SET IS ", type(set_of_vars))

            prev_vars = set_of_vars
            index += 1
            live_index += 1

            print("PRINTING FOR THIS ITERATION")
            for elem in live_var:
                print (elem)
            print("ENDING THIS ITERATION \n")

        index = 0
        for elem in live_var:
            print("LENGTH OF ELEM IS ", len(elem))
            print(elem, " --- ", live_var[index])
            index += 1

        exit(1)
        instr.reverse()
        return live_var1;


    def assign_homes(instr, var_env):
        # Go through instructions one by one to remove vars
        for i in instr:
            i.assign_homes(var_env)

        return;

    def patch(instr):
        # Return an updated list of instructions
        new_instr = []

        # Go through instructions one by one to remove invalid memory references
        for i in instr:
                # If instruction is addq, movq, or subq, then check if the first argument is a
                # memory reference, then create a movq(arg, rax) instruction
                if( (isinstance(i, addq)) or (isinstance(i, subq)) or (isinstance(i, movq)) ):
                    next = i.patch()
                    # Next might be a list, so we need to use the + operator
                    if ( isinstance(next, list)):
                        new_instr = new_instr + next
                    else:
                        # We don't actually need patch functions for other instructions, but they
                        # still exist in the case I need to change something and for consistency
                        new_instr.append(i.patch())
                else:
                    new_instr.append(i)

        return new_instr;

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
        print("addq(", end = "")

        # Check if arg is a memory address
        if (isinstance(self._arg1, xmem)):
            src = self._arg1.interp()
            src = xprog.ms.find(src)
            print("xmem(", self._arg1.interp(), ")", ",", end = "")
        else:
            src = self._arg1.interp()
            if not isinstance(src, int):
                src = xprog.ms.find(src)
            print(src, ",", end = "")

        if (isinstance(self._arg2, xmem)):
            result = self._arg2.interp()
            result = xprog.ms.find(result)
            print("xmem(", self._arg2.interp(), "))")
        else:
            result = self._arg2.interp()
            if not isinstance(result, int):
                result = xprog.ms.find(result)
            print(result, ")")

        # [ dst -> ms(src) + ms(src)]
        result += src
        xprog.ms.insert(self._arg2.interp(), result)
        return;

    def live_analysis(self, prev_vars):
        print("Addq prev_vars:", prev_vars)
        # Check if no registers are available
        if(len(xprog.reg_set) == 0):
            print("hi")
            return prev_vars;

        if(isinstance(self._arg1, xvar)):
            print("hey")
            var1 = self._arg1._var
            print(var1)
            if(var1 not in prev_vars):
                # A register is free, so assign this var to it
                #prev_vars.append(var1)
                #prev_vars.append(xprog.reg_set[0])
                temp = [var1]
                temp.append(xprog.reg_set[0])
                print(temp)
                if (prev_vars == []):
                    prev_vars = temp
                else:
                    prev_vars = [temp, prev_vars]
                print("append ", prev_vars)
                del xprog.reg_set[0]

        # Check if no registers are available after adding arg1
        if(len(xprog.reg_set) == 0):
            print("yo")
            return prev_vars;

        if(isinstance(self._arg2, xvar)):
            print("sup")
            var2 = self._arg2._var
            if(var2 in prev_vars):
                # If var is already in a register, then return
                return prev_vars;
            else:
                # A register is free, so assign this var to it
                #prev_vars.append(var2)
                #prev_vars.append(xprog.reg_set[0])
                temp = [var2]
                temp.append(xprog.reg_set[0])
                print(temp)
                if (prev_vars == []):
                    prev_vars = temp
                else:
                    prev_vars = [temp, prev_vars]
                print("append ", prev_vars)

                del xprog.reg_set[0]
                return prev_vars;

        return prev_vars;

    def assign_homes(self, var_env):
        # Remove Variables
        self._arg1 = self._arg1.assign_homes(var_env)
        self._arg2 = self._arg2.assign_homes(var_env)
        return;

    def patch(self):
        # Check if arg1 is a memory reference
        if( isinstance(self._arg1, xmem) ):
            return [movq(self._arg1, xreg("rax")), addq(xreg("rax"), self._arg2)];

        return addq(self._arg1, self._arg2);

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
        print("subq(", end = "")

        # Check if arg is a memory address
        if( isinstance(self._arg1, xmem) ):
            print("xmem(", self._arg1.interp(), ")", ",", end = "")
            src = self._arg1.interp()
            src = xprog.ms.find(src)
        else:
            src = self._arg1.interp()
            if not isinstance(src, int):
                src = xprog.ms.find(src)
            print(src, ",", end = "")

        if ( isinstance( self._arg2, xmem) ):
            result = self._arg2.interp()
            result = xprog.ms.find(result)
            print("xmem(", self._arg2.interp(), "))")
        else:
            result = self._arg2.interp()
            if not isinstance(result, int):
                result = xprog.ms.find(result)
            print(result, ")")

        # [ dst -> ms(src) + ms(src)]
        result -= src
        xprog.ms.insert(self._arg2.interp(), result)

        return;

    def live_analysis(self, prev_vars):
        # Check if no registers are available
        if(len(xprog.reg_set) == 0):
                return prev_vars;

        if(isinstance(self._arg1, xvar)):
            var1 = self._arg1._var
            if(var1 not in prev_vars):
                # A register is free, so assign this var to it
                #prev_vars.append(var1)
                #prev_vars.append(xprog.reg_set[0])
                temp = [var1]
                temp.append(xprog.reg_set[0])
                print(temp)
                if (prev_vars == []):
                    prev_vars = temp
                else:
                    prev_vars = [temp, prev_vars]
                print("append ", prev_vars)
                del xprog.reg_set[0]

        # Check if no registers are available after adding arg1
        if(len(xprog.reg_set) == 0):
                return prev_vars;

        if(isinstance(self._arg2, xvar)):
            var2 = self._arg2._var
            if(var2 in prev_vars):
                # If var is already in a register, then return
                return prev_vars;
            else:
                # A register is free, so assign this var to it
                #prev_vars.append(var2)
                #prev_vars.append(xprog.reg_set[0])
                temp = [var2]
                temp.append(xprog.reg_set[0])
                print(temp)
                if (prev_vars == []):
                    prev_vars = temp
                else:
                    prev_vars = [temp, prev_vars]
                print("append ", prev_vars)
                del xprog.reg_set[0]
                return prev_vars;

        return prev_vars;

    def assign_homes(self, var_env):
        # Remove Variables
        self._arg1 = self._arg1.assign_homes(var_env)
        self._arg2 = self._arg2.assign_homes(var_env)
        return;

    def patch(self):
        # Check if arg1 is a memory reference
        if( isinstance(self._arg1, xmem) ):
            return [movq(self._arg1, xreg("rax")), subq(xreg("rax"), self._arg2)];

        return subq(self._arg1, self._arg2);

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
        print("movq(", end = "")

        # Check if arg is a memory address
        if( isinstance(self._arg1, xmem)):
            value = self._arg1.interp()
            value = xprog.ms.find(value)
            print("xmem(", self._arg1.interp(), ")", ",", end = "")
        else:
            value = self._arg1.interp()
            if not isinstance(self._arg1, xnum):
                value = xprog.ms.find(value)
            print(value, ",", end = "")

        destination = self._arg2.interp()
        print(destination, "))")

        # movq ms' = ms[dst -> ms(src)]
        xprog.ms.insert(destination, value)
        return;

    def live_analysis(self, prev_vars):
        # Check if no registers are available
        if(len(xprog.reg_set) == 0):
            # See if var is hold a register
            if(isinstance(self._arg2, xvar)):
                var2 = self._arg2._var
                if(var2 in prev_vars):
                    print("TRYING TO DELETE")
                    # Add the register back to the reg set
                    xprog.reg_set.append(prev_vars.index(var2) + 1)
                    # Delete the var and it's corresponding register
                    del prev_vars[prev_vars.index(var2) + 1]
                    del prev_vars[prev_vars.index(var2)]
                else:
                    # It's not holding a register so just return
                    return prev_vars;
            else:
                # We can't free up a register so just return
                return prev_vars;


        if(isinstance(self._arg2, xvar)):
            print("ARG2 IS A , ", type(self._arg2), " ", self._arg2._var)
            var2 = self._arg2._var
            temp = prev_vars
            for vars in temp:
                if(var2 in vars):
                    print("TRYING TO DELETE")
                    # Add the register back to the reg set
                    xprog.reg_set.append(vars.index(var2) + 1)
                    # Delete the var and it's corresponding register
                    #del prev_vars[prev_vars.index(var2) + 1]
                    #del prev_vars[prev_vars.index(var2)]
                    del temp[temp.index(vars)]
                    prev_vars = temp

        if(isinstance(self._arg1, xvar)):
            var1 = self._arg1._var
            if(var1 in prev_vars):
                # If var is already in a register, then return
                return prev_vars;
            else:
                # A register is free, so assign this var to it
                #prev_vars.append(var1)
                #prev_vars.append(xprog.reg_set[0])
                temp = [var1]
                temp.append(xprog.reg_set[0])
                print(temp)
                if (prev_vars == []):
                    prev_vars = temp
                else:
                    prev_vars = [temp, prev_vars]
                print("append ", prev_vars)
                del xprog.reg_set[0]
                return prev_vars;

        return prev_vars;

    def assign_homes(self, var_env):
        # Remove Variables
        self._arg1 = self._arg1.assign_homes(var_env)
        self._arg2 = self._arg2.assign_homes(var_env)
        return;

    def patch(self):
        # Check if arg1 is a memory reference
        if( isinstance(self._arg1, xmem) ):
            return [movq(self._arg1, xreg("rax")), movq(xreg("rax"), self._arg2)];

        return movq(self._arg1, self._arg2);

########################## Retq #########################################################

class retq(xinstr):

    def __init__(self):
        pass

    def emitter(self, file):
        file.write("retq")
        return;

    def interp(self):
        # This should be the last instruction
        print("retq(", xprog.ms.find("rax"), ")")
        return xprog.ms.find("rax");

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        return;

    def patch(self):
        return;

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
        print("negq(", self._arg.interp(), ")")
        return;

    def live_analysis(self, prev_vars):
        # Check if no registers are available
        if(len(xprog.reg_set) == 0):
                return prev_vars;

        if(isinstance(self._arg, xvar)):
            var1 = self._arg._var
            if(var1 not in prev_vars):
                # A register is free, so assign this var to it
                #prev_vars.append(var1)
                #prev_vars.append(xprog.reg_set[0])
                temp = [var1]
                temp.append(xprog.reg_set[0])
                print(temp)
                if (prev_vars == []):
                    prev_vars = temp
                else:
                    prev_vars = [temp, prev_vars]
                print("append ", prev_vars)
                del xprog.reg_set[0]

        return prev_vars;

    def assign_homes(self, var_env):
        # Remove Variables
        self._arg = self._arg.assign_homes(var_env)
        return;

    def patch(self):
        return;

########################## Callq ########################################################

class callq(xinstr):
    def __init__(self, label):
        self._label = label

    def emitter(self, file):
        # Check if callq is for print int
        if((self._label == "_print_int") or (self._label == "print_int")):
            file.write("callq print_int")
        elif(self._label == "begin"):
            file.write("callq begin")
        else:
            # rax is the default label for callq
            file.write("callq %rax")

        return;

    def interp(self):
        # Check if callq is for print int
        if((self._label == "_print_int") or (self._label == "print_int") or (self._label == "begin")):
            return;
        else:
            src = input("Please enter a numerical value: ")
            src = int(src)

            xprog.ms.insert("rax", src)
            return;

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        return;

    def patch(self):
        return;

########################## Jmp ##########################################################

class jmp(xinstr):
    def __init__(self, label):
        self._label = label

    def emitter(self, file):
        file.write("jmp " + str(self._label) + "\n")
        print("jmp ", self._label)
        xblock.emitter(file, self._label)
        return;

    def interp(self):
        return xblock.interp(self._label);

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        return;

    def patch(self):
        return;

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
        print("pushq(", self._arg.interp(), ")")
        return;

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        # Remove Variable
        self._arg = self._arg.assign_homes(var_env)
        return;

    def patch(self):
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
        print("popq(", self._arg.interp(), ")")
        return;

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        # Remove Variable
        self._arg = self._arg.assign_homes(var_env)
        return;

    def patch(self):
        return;

########################## Arg ##########################################################

class xarg:
    def emitter():
        return 0;
    def live_analysis(self, prev_vars):
        return prev_vars;
    def assign_homes(self, var_env):
        return;
    def patch(self):
        return;

########################## X0 Number ####################################################

class xnum(xarg):
    def __init__(self, num):
        self._num = num

    def emitter(self, file):
        file.write("$" + str(self._num));
        return;

    def interp(self):
        return self._num;

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        # Return a xnum object
        return xnum(self._num);

    def patch(self):
        return;

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

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        # Return a xreg object
        return xreg(self._reg);

    def patch(self):
        return;

########################## Memory #######################################################

class xmem(xarg):
    def __init__(self, reg, offset):
        self._reg = reg
        self._offset = offset

    def emitter(self, file):
        #file.write("%" + self._reg + "(" + str(self._offset) + ")");
        file.write(str(self._offset) + "(%" + self._reg + ")")
        return;

    def interp(self):
        # Look up value from the register
        address = xprog.ms.find(self._reg)

        # Look up value + offset in address mapping in machine state
        address = address + self._offset

        return address;

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        return;

    def patch(self):
        return;

########################## X0 Var #######################################################

class xvar(xarg):
    def __init__(self, var):
        self._var = var

    def emitter(self, file):
        file.write("(" + self._var + ")")
        return;

    def interp(self):
        return self._var;

    def live_analysis(self, prev_vars):
        return prev_vars;

    def assign_homes(self, var_env):
        # Return the memory address for the corresponding variable
        return var_env.find_var(self._var);

    def patch(self):
        return;
