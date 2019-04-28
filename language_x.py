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
import shutil
import copy

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

        file_name = "test_" + str(xprog.num_of_tests)
        if(os.path.isdir(file_name) is False):
            os.mkdir(file_name)
        else:
            shutil.rmtree(file_name)
            os.mkdir(file_name)

        os.chdir(cur_path + "/assembly_tests/" + file_name)
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

    def color_graph(self, debug = False, move_flag = False):
        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        build_graph = self._info["build_interference"]
        move_graph = self._info["move_graph"]

        # Holds color graph
        saturation_graph = {}

        saturation_graph = xblock.color_graph("main", build_graph, saturation_graph, move_graph, move_flag)

        if debug:
            print("ANSWER:")
            i = 0
            for n in saturation_graph:
                # Don't print register values
                if ( i > 12):
                    print(n,":",saturation_graph[n], end=" ")
                i += 1
            print()

        self._info["color_graph"] = saturation_graph

        return xprog(self._info, self._label_map);

    # Checks for interference between two variables to increase effiency for
    # register allocation
    def build_interference(self, debug = False):
        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        # Grab instructions from live analysis
        live_instr = self._info["live"]

        # Holds the graph of build interference for all instructions. Python documentation
        # recommends using dictionaries to make simple graphs
        build_graph = {}

        # Holds graph for Move Biasing
        move_graph = {}

        build_graph = xblock.build_interference("main", live_instr, build_graph, move_graph)

        if ( debug ):
            print ("BUILD INTERFERENCE:")
            for keys in build_graph:
                print (keys, "->", build_graph[keys])
            print ("MOVE GRAPH:")
            for keys in move_graph:
                print (keys, "->", move_graph[keys])

        self._info["build_interference"] = build_graph
        self._info["move_graph"] = move_graph

        return xprog(self._info, self._label_map);

    # Takes an X program and returns a set of all the variables assigned to registers
    def live_analysis(self, debug = False):

        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        # Holds the sets of all of the variables and their correpsonding registers
        # Register can be r8 through r15
        live_set = []

        # Holds all the available registers
        xprog.reg_set = ["r8", "r9", "r10", "r11", "r12", "r15"]

        # Perform analysis on main and any other labels jumped to
        live_set = xblock.live_analysis("main", live_set, debug)

        if( self._info is None ):
            self._info = {}

        self._info["live"] = live_set

        return xprog(self._info, self._label_map);

    # Takes a X prog w/ vars, and returns a xprog w/o vars
    def assign_registers(self):

        if ( "uncover" in self._info):
            # Contains all variables in program
            all_vars = self._info["uncover"]
        else:
            all_vars = self._info

        # Create a new enviroment that contains the address of each
        # variable on the stack
        var_env = env()

        # Holds Variable Count
        vc = 0

        # Check for color graph pass
        if ("color_graph" in self._info):
            g = self._info["color_graph"]
            r = ["rdx", "rcx", "rsi", "rdi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
            byte_count = 8
            for vars in all_vars:
                # If var exists in graph, and it's a register
                if((vars in g) and (g[vars] < len(r))):
                    # g[vars] is the color assigned, which is a one to one of the list r
                    n = g[vars]
                    var_env.add_var(vars, xreg(r[n]))

                # If neither condition is met, then add to stack
                else:
                    var_env.add_var(vars, xmem("rsp", byte_count))
                    byte_count += 8
                    vc += 1

            old_vc = vc
            vc = vc * 8
            # Make sure memory size for variables is divisible by 16
            if (vc % 16 != 0):
                vc = ((old_vc) + 1) * 8

        # Still support legacy code
        else:
            byte_count = 8
            for vars in all_vars:
                # Add memory address on the stack for current var
                var_env.add_var(vars, xmem("rsp", byte_count))
                byte_count += 8

            # Find number of variables to push to stack and adjust for memory size
            vc = len(self._label_map) * 8

            # Make sure memory size for variables is divisible by 16
            if (vc % 16 != 0):
                vc = (len(self._label_map) + 1) * 8

        # Instructions to start program
        begin_instr =\
        [ pushq(xreg("rbp")),\
        movq(xreg("rsp"), xreg("rbp")),\
        pushq(xreg("r12")),\
        pushq(xreg("r13")),\
        pushq(xreg("r14")),\
        pushq(xreg("r15")),\
        subq(xnum(vc), xreg("rsp")),\
        jmp("next")
        ]
        self._label_map["begin"] = begin_instr

        # ** I changed subq to to addq in begin, and vice versa in end. Not sure if this **
        # ** should be changed **

        # Instructions to end program
        end_instr =\
        [ addq(xnum(vc), xreg("rsp")),\
        popq(xreg("r15")),\
        popq(xreg("r14")),\
        popq(xreg("r13")),\
        popq(xreg("r12")),\
        popq(xreg("rbp")),\
        retq()
        ]
        self._label_map["end"] = end_instr

        # Set Label Map for Machine State Zero
        xprog.ms._label_map = self._label_map

        xblock.assign_registers("main", var_env)

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

    def color_graph(label, build_graph, saturation_graph, move_graph, move_flag = False):
        # Set current block
        xprog.ms._block = xprog.ms._label_map[label]

        saturation_graph = xinstr.color_graph(xprog.ms._block, build_graph, saturation_graph, move_graph, move_flag)

        return saturation_graph;

    def build_interference(label, live_instr, build_graph, move_graph):
        # Set current block
        xprog.ms._block = xprog.ms._label_map[label]

        build_graph = xinstr.build_interference(xprog.ms._block, live_instr, build_graph, move_graph)

        return build_graph;

    def live_analysis(label, live_set, debug = False):
        # Set current block
        xprog.ms._block = xprog.ms._label_map[label]

        # Holds the list of instructions for this block
        live_var = []
        live_set = live_set + xinstr.live_analysis(xprog.ms._block, live_var)

        # Print out every analysis for each instruction
        if (debug):
            print("LABEL: ", label)
            for l in live_var:
                print (l)

        return live_set;

    def assign_registers(label, var_env):
        # Update instruction block
        xprog.ms._block = xprog.ms._label_map[label]

        xinstr.assign_registers(xprog.ms._block, var_env)
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

    # Helper function so that if a new color is found, we can look back over the whole list recursively
    # ** Temp Graph is a Dictionary & Known Colors is a List **
    # Helper function so that if a new color is found, we can look back over the whole list recursively
    def color_graph_helper(colors, known_colors, new_color = 0):

        # For every color adjacent to primary node
        for c in known_colors:
            # If an adjacent node already has "new_color", then increment, and look back over the list
            if(known_colors[known_colors.index(c)] == new_color):
                print("THIS VALUE IS ", known_colors[known_colors.index(c)])
                new_color += 1
                new_color = xinstr.color_graph_helper(colors, known_colors, new_color);

        return new_color;


    def color_graph(instr, build_graph, saturation_graph, move_graph, move_flag = False):
        # Holds a priority queue from the most saturated to the least saturated
        queue = []

        # Fill out priority queue
        for keys in build_graph:
            # Base case
            if (len(queue) == 0):
                queue.append(keys)
            else:
                i = 0
                temp = build_graph[keys]
                next = queue[i]
                # Go through queue, while priority is higher than current key (temp)
                # Priority == Length of List
                while ( (i < len(queue)) and (len(temp) < len(build_graph[next])) ):
                    next = queue[i]
                    i += 1
                # Insert key into queue based on priority
                queue.insert(i, keys)

        # Keeps track of the lowest color used. Registers are by default precolored
        colors = {"rdx":0, "rcx":1, "rsi":2, "rdi":3, "r8":4, "r9":5, "r10":6, "r11":7, "r12":8,\
        "r13":9, "r14":10, "r15":11}

        # From highest priority (saturation) to lowest priority
        for v in queue:

            # u is a list of nodes attached to v
            u = build_graph[v]

            # Keep track of known colors
            known_colors = []

            # adj is the adjacent nodes listed in u
            for adj in u:
                if (adj in colors):
                    known_colors.append(colors[adj])

            # Check for adjacent nodes by looking at other nodes that mention this node
            for b in build_graph:
                temp = build_graph[b]
                if ((v in temp) and (b in colors)):
                    known_colors.append(colors[b])

            # Create a deep copy of move graph so we can avoid data being manipulated by pointers
            if((move_flag) and (v in move_graph)):

                # Create a list based off of new move graph
                move_list =[]
                temp_graph = move_graph[v]
                highest_color = 0
                print("ALL IN MOVE ", temp_graph)
                print("ALL IN U ", u)
                exit(1)
                for m in temp_graph:
                    if(m not in u):
                        move_list.append(m)
                        if ( (m in colors) and (colors[m] > highest_color)):
                            highest_color = colors[m]
                        print("APPENDING ", m)

                colors[v] = xinstr.color_graph_helper(colors, move_list)
                print("COLOR WITH BIASE IS ", colors[v])
                if(colors[v] > highest_color):
                    color[v] = xinstr.color_graph_helper(colors, known_colors)
            else:
                # Call helper function to find color for node
                colors[v] = xinstr.color_graph_helper(colors, known_colors)
                print("COLOR WITHOUT BIASE IS ", colors[v])

        saturation_graph = colors

        return saturation_graph;

    def build_interference(instr, live_instr, build_graph, move_graph):
        # Index for current instruction
        index = 0

        # All special registers
        special_regs = [xreg("rdx"), xreg("rcx"), xreg("rsi"), xreg("rdi"),\
        xreg("r8"), xreg("r9"), xreg("r10"), xreg("r11"), xreg("r12"), xreg("r13"), xreg("14"), xreg("15")]

        for i in live_instr:
            curr_instr = instr[index]
            #Skip instruction if it is empty
            if(i != []):

                # Check if instruction is addq or subq
                if((isinstance(curr_instr, addq)) or (isinstance(curr_instr, subq))):
                    # Go through each variable in current instruction
                    k = 0
                    for vars in i:
                        if ( vars != []):
                            # Format for live instr is var -> reg -> var -> reg...
                            if( (k % 2) == 0 ):
                                # Check to make sure variable isn't destination
                                if( vars != curr_instr._arg2.interp() ):
                                    if ( vars not in build_graph ):
                                        build_graph[vars] = [curr_instr._arg2.interp()]
                                    else:
                                        if(curr_instr._arg2.interp() not in build_graph[vars]):
                                            temp = build_graph[vars]
                                            build_graph[vars] = temp + [curr_instr._arg2.interp()]
                        k += 1
                # Check if instruction is addq or subq
                if(isinstance(curr_instr, negq)):
                    k = 0
                    for vars in i:
                        if( vars != []):
                            if( (k % 2) == 0):
                                # Format for live instr is var -> reg -> var -> reg...
                                if(vars != curr_instr._arg.interp()):
                                    if(vars not in build_graph):
                                        build_graph[vars] = [curr_instr._arg.interp()]
                                    else:
                                        if(curr_instr._arg.interp() not in build_graph[vars]):
                                            temp = build_graph[vars]
                                            build_graph[vars] = temp + [curr_instr._arg.interp()]
                        k += 1

                # Check if instruction is movq
                if(isinstance(curr_instr, movq)):
                    k = 0
                    # Go through each variable in current instruction
                    for vars in i:
                        if ( vars != []):
                            if ( (k % 2) == 0 ):
                                if ((vars != curr_instr._arg1.interp()) and (vars != curr_instr._arg2.interp())):
                                    # Check if vars has already been added to build graph
                                    if ( vars not in build_graph ):
                                        build_graph[vars] = [curr_instr._arg2.interp()]
                                        move_graph[vars] = [curr_instr._arg2.interp()]
                                    else:
                                        if(curr_instr._arg2.interp() not in build_graph[vars]):
                                            build_temp = build_graph[vars]
                                            build_graph[vars] = build_temp + [curr_instr._arg2.interp()]
                                            move_temp = move_graph[vars]
                                            move_graph[vars] = move_temp + [curr_instr._arg2.interp()]
                        k += 1

                # Check if instruction is callq and add caller-saved special registers
                if((isinstance(curr_instr, callq)) or (isinstance(curr_instr, jmp)) or (isinstance(curr_instr, retq))\
                or (isinstance(curr_instr, pushq)) or (isinstance(curr_instr, popq))):
                    k = 0
                    # Go through each variable in current instruction and attach special registers
                    for vars in i:
                        if ( vars != []):
                            if ((k % 2) == 0):
                                if ( vars not in build_graph ):
                                    build_graph[vars] = special_regs
                                else:
                                    if(special_regs not in build_graph[vars]):
                                        temp = build_graph[vars]
                                        build_graph[vars] = temp + special_regs
                        k += 1

            index += 1

        return build_graph;

    def live_analysis(instr, live_var):
        # Instruction count
        index = 0

        # Reverse instruction set
        instr.reverse()

        # Holds the previous set of registers and variables
        prev_vars = []

        # Go through each instruction
        while (index < len(instr)):
            # Assign temp the next instruction
            temp = instr[index]

            # Instruction is either addq or subq
            if((isinstance(temp, addq) or (isinstance(temp, subq)))):
                # Check if no registers are available and arg1 is a var
                if((len(xprog.reg_set) != 0) and (isinstance(temp._arg1, xvar))):
                    var = temp._arg1._var
                    if(var not in prev_vars):
                        # A register is free, so assign this var to it
                        prev_vars.insert(0, var)
                        prev_vars.insert(1, xprog.reg_set[0])
                        del xprog.reg_set[0]

                # Check if no registers are available and arg2 is a var
                if((len(xprog.reg_set) != 0) and (isinstance(temp._arg2, xvar))):
                    var = temp._arg2._var
                    if(var not in prev_vars):
                        # A register is free, so assign this var to it
                        prev_vars.insert(0, var)
                        prev_vars.insert(1, xprog.reg_set[0])
                        del xprog.reg_set[0]

            # Instruction is a movq
            if(isinstance(temp, movq)):
                # Delete register attached to arg2 if possible first to free up a register
                if(isinstance(temp._arg2, xvar)):
                    var = temp._arg2._var
                    if(var in prev_vars):
                        xprog.reg_set.insert(0, prev_vars[prev_vars.index(var) + 1])
                        del prev_vars[prev_vars.index(var) + 1]
                        del prev_vars[prev_vars.index(var)]

                if((len(xprog.reg_set) != 0) and (isinstance(temp._arg1, xvar))):
                    var = temp._arg1._var
                    if(var not in prev_vars):
                        prev_vars.insert(0, var)
                        prev_vars.insert(1, xprog.reg_set[0])
                        del xprog.reg_set[0]

            # Instruction is a negq
            if(isinstance(temp, negq)):
                # Add variable to register if there is space
                if((len(xprog.reg_set) != 0) and (isinstance(temp._arg, xvar))):
                    var = temp._arg._var
                    if(var not in prev_vars):
                        prev_vars.insert(0, var)
                        prev_vars.insert(1, xprog.reg_set[0])
                        del xprog.reg_set[0]


            # Start appending variables and registers for this instruction
            if (prev_vars == []):
                # Check if instruction is first in the list
                if((index + 1) == len(instr)):
                    live_var.append(live_var[index-1])
                else:
                    live_var.append([])
            else:
                # Check if instruction is the first in the list
                if((index + 1) == len(instr)):
                    live_var.append(live_var[index-1])
                else:
                    live_var.append(prev_vars[:])

            index += 1

        live_var.reverse()
        instr.reverse()
        return live_var;


    def assign_registers(instr, var_env):
        # Go through instructions one by one to remove vars
        for i in instr:
            i.assign_registers(var_env)

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
                        new_instr.append(next)
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

    def assign_registers(self, var_env):
        # Remove Variables
        self._arg1 = self._arg1.assign_registers(var_env)
        self._arg2 = self._arg2.assign_registers(var_env)
        return;

    def patch(self):
        # Check if arg1 is a memory reference
        if( (isinstance(self._arg1, xmem)) and (isinstance(self._arg2, xmem)) ):
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

    def assign_registers(self, var_env):
        # Remove Variables
        self._arg1 = self._arg1.assign_registers(var_env)
        self._arg2 = self._arg2.assign_registers(var_env)
        return;

    def patch(self):
        # Check if arg1 is a memory reference
        if( (isinstance(self._arg1, xmem)) and (isinstance(self._arg2, xmem)) ):
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

    def assign_registers(self, var_env):
        # Remove Variables
        self._arg1 = self._arg1.assign_registers(var_env)
        self._arg2 = self._arg2.assign_registers(var_env)
        return;

    def patch(self):
        # Check if arg1 is a memory reference
        if( (isinstance(self._arg1, xmem)) and (isinstance(self._arg2, xmem)) ):
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

    def assign_registers(self, var_env):
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

    def assign_registers(self, var_env):
        # Remove Variables
        self._arg = self._arg.assign_registers(var_env)
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
        if((self._label == "_print_int") or (self._label == "print_int")):
            return;
        elif (self._label == "begin"):
            return xblock.interp(self._label)
        else:
            src = input("Please enter a numerical value: ")
            src = int(src)

            xprog.ms.insert("rax", src)
            return;

    def assign_registers(self, var_env):
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

    def assign_registers(self, var_env):
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

    def assign_registers(self, var_env):
        # Remove Variable
        self._arg = self._arg.assign_registers(var_env)
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

    def assign_registers(self, var_env):
        # Remove Variable
        self._arg = self._arg.assign_registers(var_env)
        return;

    def patch(self):
        return;

########################## Arg ##########################################################

class xarg:
    def emitter():
        return 0;
    def assign_registers(self, var_env):
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

    def assign_registers(self, var_env):
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

    def assign_registers(self, var_env):
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

    def assign_registers(self, var_env):
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

    def assign_registers(self, var_env):
        # Return the memory address for the corresponding variable
        return var_env.find_var(self._var);

    def patch(self):
        return;
