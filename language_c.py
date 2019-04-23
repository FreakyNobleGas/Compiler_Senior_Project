#
#    Nick Quinn - Compiler Construction
#
#   This file describes and implements the C language.
#
# Language C0:
#
# p := (program info [label -> tail] ... )
# tail := (return arg) | (seq stmt tail)
# stmt := set var expr
# expr := arg | (read) | (-arg) | (+ arg arg)
# arg := number | var
#

from language_x import *
from support import *

#########################################################################################
##########################        C0 Language           #################################
#########################################################################################

########################## C Program ####################################################
class cprog():
    # Dictionary to hold all vars -> (x...)
    info_dict = {}
    # Mapping for select pass
    label_map = {}

    # Program = (Program Info [label->tail])
    def __init__(self, info, label):
        self._info = info
        self._label = label

    def interp(self):
        # Empty enviroment
        cenv = env()

        try:
            instr = self._label["main"]
        except KeyError:
            instr = self._label["middle"]

        return print("return ", ctail.interp(cenv, instr), "\n")

    # Requires that ECON and RCO have passed
    def uncover(self):
        # Reinitialize info dictionary
        cprog.info_dict.clear()

        # Initialize empty enviroment
        cenv = env()

        # middle is label created by ECON
        instr = self._label["middle"]

        ctail.uncover(cenv, instr)

        if ( self._info is None ):
            self._info = {}
            
        self._info["uncover"] = cprog.info_dict
        return cprog(self._info, self._label);

    # Takes a C program and returns a X0 program
    def select(self):
        # Reinitialize mapping
        cprog.label_map.clear()
        # List of C instructions
        c_instr = self._label["middle"]
        # Empty List to hold new X instructions
        x_instr = []
        # New enviroment
        cenv = env()

        # Go through C program and create X program
        x_instr = ctail.select(cenv, c_instr, x_instr)

        # Select will return the x_instr list
        cprog.label_map["main"] = x_instr

        # After rco, every program will have at least one variable so we will need this
        # label for now
        end_instr = [retq()]
        cprog.label_map["end"] = end_instr

        return xprog(self._info, cprog.label_map);


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

        return "Error: No return statement in interp.";

    def uncover(cenv, instr):
        for i in instr:
            if isinstance(i, cstmt):
                # sequence stmt tail
                i.uncover(cenv)
            else:
                return;

        return "Error: No return statement in uncover.";

    def select(cenv, c_instr, x_instr):
        for i in c_instr:
            if isinstance(i, cstmt):
                # sequence stmt tail
                x_instr = i.select(cenv, c_instr, x_instr)
            else:
                # Last instruction, should be a return so we will jump to a new label
                # since we do not know how many local variales are in the stack
                dst = None
                arg = i.select(cenv, c_instr, x_instr, dst)
                x_instr.append(movq(arg, xreg("rax")))
                x_instr.append(jmp("end"))
                #i.select(cenv, c_instr, x_instr, dst)
                return x_instr;

        return "Error: No return statement in select.";

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

    def uncover(self, cenv):
        cprog.info_dict[self._var] = self._expr

        # Call to uncover from here is strictly for pretty print feature
        if(self._var.startswith("_")):
            print(self._var, " = ", self._expr.uncover(cenv))
        else:
            print(" " + self._var, " = ", self._expr.uncover(cenv))
        return;

    def select(self, cenv, c_instr, x_instr):
        dst = xvar(self._var)
        x_instr = self._expr.select(cenv, c_instr, x_instr, dst)
        return x_instr;

########################## C Expression #################################################
class cexpr():
    # Expression = arg | (read) | (-arg) | (+ arg arg)
    def __init__(self, arg):
        self._arg = arg

    def interp(self, cenv):
        return self._arg.interp(cenv);

    def uncover(self, cenv):
        #print("Error: cexpr was hit in uncover-locals function.")
        return self._arg.uncover(cenv);

    def select(self, cenv, c_instr, x_instr, dst):
        x_instr = self._arg.select(cenv, c_instr, x_instr, dst)
        return x_instr;


########################## C Read #######################################################
class cread():
    def __init__(self):
        pass

    def interp(self, cenv):
        num = input("Please enter a numerical value: ")
        self._num = int(num)
        print(" read ", self._num, " ")
        return self._num;

    def uncover(self, cenv):
        #print("Error: cread was hit in uncover-locals function.")
        return "Read()";

    def select(self, cenv, c_instr, x_instr, dst):
        x_instr.append(callq("_read_int"))
        x_instr.append(movq("rax", dst))
        return x_instr;

########################## C Negate #####################################################
class cneg():
    def __init__(self, arg):
        self._arg = arg

    def interp(self, cenv):
        result = self._arg.interp(cenv)
        result *= -1
        print("Neg(", result, ")")
        return result

    def uncover(self, cenv):
        #print("Error: cneg was hit in uncover-locals function.")
        return "cneg(" + str(self._arg) + ")";

    def select(self, cenv, c_instr, x_instr, dst):
        # Retrieve actual argument value from carg object
        if(isinstance(self._arg, carg)):
            self._arg = self._arg._arg

        if(isinstance(self._arg, int)):
            x_instr.append(movq(xnum(self._arg), dst))
        else:
            x_instr.append(movq(xvar(self._arg), dst))

        x_instr.append(negq(dst))
        return x_instr;

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

    def uncover(self, cenv):
        #print("Error: cadd was hit in uncover-locals function.")

        if(isinstance(self._arg1, carg) and isinstance(self._arg2, carg)):
            return "add(" + str(self._arg1.uncover(cenv)) + "," + str(self._arg2.uncover(cenv)) + ")";

    def select(self, cenv, c_instr, x_instr, dst):
        # Retrieve actual argument value from carg object
        if(isinstance(self._arg1, carg)):
            self._arg1 = self._arg1._arg
        if(isinstance(self._arg2, carg)):
            self._arg2 = self._arg2._arg

        if(isinstance(self._arg2, int)):
            x_instr.append(movq(xnum(self._arg2), dst))
        else:
            x_instr.append(movq(xvar(self._arg2), dst))

        if(isinstance(self._arg1,int)):
            x_instr.append(addq(xnum(self._arg1), dst))
        else:
            x_instr.append(addq(xvar(self._arg1), dst))

        return x_instr;

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

    # I do not believe carg needs to be implemented for uncover-locals to work. I may need to
    # change this in the future.
    def uncover(self, cenv):
        #print("Error: carg was hit in uncover-locals function.")
        return "carg(" + str(self._arg) + ")";

    def select(self, cenv, c_instr, x_instr, dst):
        if(dst is None):
            if(isinstance(self._arg, int)):
                return xnum(self._arg);
            else:
                return xvar(self._arg);
        else:
            if(isinstance(self._arg, int)):
                x_instr.append(movq(xnum(self._arg), dst))
                return x_instr;
            else:
                x_instr.append(movq(xvar(self._arg), dst))
                return x_instr;
