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
