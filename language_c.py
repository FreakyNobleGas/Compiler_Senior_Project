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

from support import *

#########################################################################################
##########################        C0 Language           #################################
#########################################################################################

########################## C Program ####################################################
class cprog():
    # Dictionary to hold all vars -> (x...)
    info_dict = {}

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
        return cprog(cprog.info_dict, self._label);

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
