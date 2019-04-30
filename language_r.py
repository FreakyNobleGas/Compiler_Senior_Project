#
#    Nick Quinn - Compiler Construction
#
#   This file describes and implements the R language.
#
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
# Language R2:
#
# e ::= ... | true | false | (and ee) | (or ee)
#       (not e) | (cmp ee) | (if e e e) | (- ee)
#
# Resolve Complex (RCO)
# p ::= (program info e)
# e ::= arg | (let x = c in e)
# c ::= read | (-arg) | (+ arg arg)
# arg ::= number | var

from language_c import *
from support import *

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
    list_of_lets = []
    body_list = []

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
    def uniq(self, unique_var, old_var):
        return 0;
    def rco(self):
        return 0;
    def econ(self):
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

    def uniq(self, unique_var, old_var):
        return;

    def rco(self):
        # Just return the number
        return num(self._num);

    def econ(self):
        return carg(self._num);

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

    def uniq(self, unique_var, old_var):
        self._num.uniq(unique_var, old_var)
        return;

    def rco(self):
        # If value is just a num or var, then save it to a new var and add to env
        if ((isinstance(self._num, num)) or isinstance(self._num, var)):
            result = self._num.rco()

            if(isinstance(result, str)):
                result = var(result)

            result_var = create_unique_var(prog.map_env)
            xprog.map_env.add_var(result_var, result)
            expr.list_of_lets.append(result_var)
        # If not just a num or a var, get the var from calling rco, all other functions
        # will return a var name
        else:
            result_var = self._num.rco()

        # Create overarching var for the result
        neg_var = create_unique_var(prog.map_env)
        prog.map_env.add_var(neg_var, neg(var(result_var)))
        expr.list_of_lets.append(neg_var)

        # Return name of overarching var
        return neg_var;

    def econ(self):
        return cneg(self._num);

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

    def uniq(self, unique_var, old_var):
        # If either side is a let, then we do not want to go further since
        # we call uniq from let for each instance of a let
        if(type(self._lhs) is not let):
            self._lhs.uniq(unique_var, old_var)
        if(type(self._rhs) is not let):
            self._rhs.uniq(unique_var, old_var)
        return;

    def rco(self):
        # Check if left hand side a num/var, else call rco again to get to a
        # num or var
        if ((isinstance(self._lhs, num)) or (isinstance(self._lhs, var))):
            lhs_var = create_unique_var(prog.map_env)
            lhs_result = self._lhs.rco()

            if(isinstance(lhs_result, str)):
                lhs_result = var(lhs_result)

            prog.map_env.add_var(lhs_var, lhs_result)
            expr.list_of_lets.append(lhs_var)
        else:
            lhs_var = self._lhs.rco()

        # Same as left hand side, now with right hand side
        if ((isinstance(self._rhs, num)) or (isinstance(self._rhs, var))):
            rhs_var = create_unique_var(prog.map_env)
            rhs_result = self._rhs.rco()

            if(isinstance(rhs_result, str)):
                rhs_result = var(rhs_result)

            prog.map_env.add_var(rhs_var, rhs_result)
            expr.list_of_lets.append(rhs_var)
        else:
            rhs_var = self._rhs.rco()

        # Create var that will add the new variables for lhs and rhs
        add_var = create_unique_var(prog.map_env)
        prog.map_env.add_var(add_var, add(var(lhs_var), var(rhs_var)))
        expr.list_of_lets.append(add_var)

        # return var in case there are more calls
        return add_var;

    def econ(self):
        return cadd(self._lhs.econ(), self._rhs.econ());


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

    def uniq(self, unique_var, old_var):
        return;

    # Ask the user for a num, and add that num to a new unique var
    def rco(self):
        num = input("Please enter a numerical value: ")
        self._num = int(num)

        read_var = create_unique_var(prog.map_env)
        prog.map_env.add_var(read_var, self._num)
        expr.list_of_lets.append(read_var)

        return read_var;

    def econ(self):
        return cread();

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
        # Check if self._x is accidently a var. If so, return to string.
        if(isinstance(self._x, var)):
            self._x = self._x._var

        # Immediately call Uniquify to avoid duplicate variables in env
        old_var = self._x
        self._x = uniquify(self._x, prog.map_env)
        self._xb.uniq(self._x, old_var)

        prog.map_env.add_var(self._x, self._xe.interp())
        return self._xb.interp()

    def opt(self):
        # Check if self._x is accidently a var. If so, return to string
        if(isinstance(self._x, var)):
            self._x = self._x._var

        # Immediately call Uniquify to avoid duplicate variables in env
        old_var = self._x
        self._x = uniquify(self._x, prog.map_env)
        self._xb.uniq(self._x, old_var)

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

    def uniq(self, unique_var, old_var):
        return;

    def rco(self):
        # Calculate XE
        if ((isinstance(self._xe, num)) or (isinstance(self._xe, var))):
            xe_var = create_unique_var(prog.map_env)
            xe_result = self._xe.rco()

            if(isinstance(xe_result, str)):
                xe_result = var(xe_result)

            prog.map_env.add_var(xe_var, xe_result)
            expr.list_of_lets.append(xe_var)
        else:
            xe_var = self._xe.rco()

        # Add X to the enviroment
        prog.map_env.add_var(self._x, var(xe_var))
        expr.list_of_lets.append(self._x)

        # Calculate XB
        if ((isinstance(self._xb, num)) or (isinstance(self._xb, var))):
            xb_var = create_unique_var(prog.map_env)
            xb_result = self._xb.rco()

            if(isinstance(xb_result, str)):
                xb_result = var(xb_result)

            prog.map_env.add_var(xb_var, xb_result)
            expr.list_of_lets.append(xb_var)
        else:
            xb_var = self._xb.rco()

        return xb_var;

    def econ(self):
        # Append C statement with x and xe
        expr.body_list.append(cstmt(self._x, self._xe.econ()))
        return self._xb.econ();

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

    def uniq(self, unique_var, old_var):
        # If var is previous name before uniquify, then change,
        # otherwise, this var is not the same.
        if(self._var == old_var):
            self._var = unique_var
        return;

    def rco(self):
        # Return the name of the variable
        return self._var;

    def econ(self):
        # Return the name of the variable
        return carg(self._var);

########################## True #########################################################
class true(expr):
    def __init__(self):
        pass

    def pretty_print(self):
        return "True";

########################## False ########################################################
class false(expr):
    def __init__(self):
        pass

    def pretty_print(self):
        return "False";

########################## Sub ##########################################################
class sub(expr):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + "-" + str(self._rhs.pretty_print()) + ")";

    # Use syntatic sugar - (+lhs (-rhs))
    #def interp(self):

########################## Or ###########################################################
class _or(expr):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + " || " +  str(self._rhs.pretty_print()) + ")";

########################## And ##########################################################
class _and(expr):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + " && " +  str(self._rhs.pretty_print()) + ")";

########################## Not ##########################################################
class _not(expr):
    def __init__(self, arg):
        self._arg = arg

    def pretty_print(self):
        return "(!" + str(self._arg.pretty_print()) + ")";

    # Not recommended to use syntatic sugar
    #def interp(self):

########################## Comparision ##################################################
class cmp(expr):
    def __init__(self, lhs, comp, rhs):
        self._lhs = lhs
        self._rhs = rhs
        # == | < | <= | > | >=
        self._comp = comp

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + str(self._comp) + str(self._rhs.pretty_print()) + ")";

########################## If ###########################################################
class _if(expr):
    # c = condition, t = true side, f = false side
    def __init__(self, c, t, f):
        self._c = c
        self._t = t
        self._f = f

    def pretty_print(self):
        return "( if " + str(self._c.pretty_print()) + " then " + str(self._t.pretty_print()) + " else " +\
               str(self._f.pretty_print()) + ")";

    #def interp(self):

########################## Prog #########################################################
# -- Inherited Class for the Program "Container" --

class prog(expr):
    # Global variable that holds the linked list that maps var->num
    map_env = env()
    debugger = ""
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

    def uniq(self, unique_var, old_var):
        print ("Error: uniq prog function should not have been hit.")
        return;

    # Helps recursively enter lets
    def rco_helper(index):
        # If last let
        if (index == (len(expr.list_of_lets) - 1)):
            vars = expr.list_of_lets[index]
            result = prog.map_env.find_var(vars)
            return let(vars, result, var(vars));

        # If not last let
        elif (index < len(expr.list_of_lets)):
            vars = expr.list_of_lets[index]
            result = prog.map_env.find_var(vars)
            return let(vars, result, prog.rco_helper(index + 1));

        # This should never be hit
        else:
            print("Error: rco_helper else block was hit.")
            return;

    def rco(self):
        # Reset list of lets
        expr.list_of_lets.clear()

        # Descends down program and determines lets by appending the names of
        # vars to list of lets
        self._e.rco()
        # Initialize first let, and then recursively enter lets using helper function
        #index = len(expr.list_of_lets) - 1
        vars = expr.list_of_lets[0]
        result = prog.map_env.find_var(vars)
        generate = let(vars, result, prog.rco_helper(1))
        return prog(None, generate);

    # Takes R programs and produces C programs
    def econ(self):
        expr.body_list.clear()

        # The return statment from calling econ should be return arg
        return_arg = self._e.econ()
        expr.body_list.append(return_arg)

        # Create a [Body -> Tail] mapping
        label_map = {"middle": expr.body_list}

        return cprog(None, label_map);
