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
import copy

#########################################################################################
##########################     R Support Functions     ##################################
#########################################################################################

########################## Optimize Helper ##############################################
# -- Helper function for R2 optimizer functions so that reads can be added for --
# -- every boolean program that uses S64                                       --
def opt_helper(opt_var):
    # Begin working on opt_var
    num_of_reads = len(expr.arry_of_reads)
    num_of_vars = expr.num_of_vars

    # This will always be an integer since read returns 0
    temp_var = opt_var.opt()
    result = num(temp_var)
    result_temp = result

    # Number of Reads counted after optomizing xe
    diff_of_reads = (len(expr.arry_of_reads) - num_of_reads)
    diff_of_vars = expr.num_of_vars - num_of_vars

    # For each read, insert a read() into opt_var
    i = 0
    while i < diff_of_reads:
        if (expr.arry_of_reads[i] == -1):
            if (result_temp == result) and (temp_var == 0):
                result = neg(read())
            else:
                result = add(neg(read()), result)
        elif (expr.arry_of_reads[i]):
            if (result_temp == result) and (temp_var == 0):
                result = read()
            else:
                result = add(read(), result)
        else:
            print("Something went wrong. Neither 1 or -1 in let opt")
        i += 1

    # Delete reads from array since we do not know if they are positive or negative
    i = 0
    while i < diff_of_reads:
        del expr.arry_of_reads[0]
        i += 1

    # For each var, insert vars into result. Var can either be a number or an expression with reads
    i = 0
    while i < diff_of_vars:
        if (expr.arry_of_vars[i][0] == "+"):
            if (result_temp == result) and (temp_var == 0):
                result = var(expr.arry_of_vars[i][1])
            else:
                result = add(var(expr.arry_of_vars[i][1]), result)
        else:
            if (result_temp == result) and (temp_var == 0):
                result = neg(var(expr.arry_of_vars[i][1]))
            else:
                result = add(neg(var(expr.arry_of_vars[i][1])), result)
        i += 1

    # Delete var from array
    i = 0
    while i < diff_of_vars:
        del expr.arry_of_vars[0]
        expr.num_of_vars -= 1
        i += 1

    return result;

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

    purity = True

    def interp(self):
        return 0;
    def pretty_print(self):
        return 0;
    def type_check(self):
        return 0;
    def opt(self):
        return 0;
    def uniq(self, unique_var, old_var):
        return 0;
    def rco(self):
        return 0;
    def econ(self):
        return 0;

########################## True #########################################################
class true(expr):
    def __init__(self):
        pass

    def pretty_print(self):
        return "True";

    def interp(self):
        return True;

    def type_check(self):
        return True;

    def opt(self):
        return True;

    def uniq(self, unique_var, old_var):
        return;

########################## False ########################################################
class false(expr):
    def __init__(self):
        pass

    def pretty_print(self):
        return "False";

    def interp(self):
        return False;

    def type_check(self):
        return False;

    def opt(self):
        return False;

    def uniq(self, unique_var, old_var):
        return;

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
        if (expr.neg_count % 2 == 0):
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

    def type_check(self):
        return self._num;

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
            prog.map_env.add_var(result_var, result)
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
        return cneg(self._num.econ());

    def type_check(self):
        # Make sure argument is an int
        check = self._num.type_check()
        if(isinstance(check, bool)):
            raise TypeCheckError("Error: Negation argument was not of type S64.")
        elif(isinstance(check, int)):
            return 1;
        else:
            raise TypeCheckError("Error: Negation argument was not of type S64.")

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

    def type_check(self):
        lcheck = self._lhs.type_check()
        rcheck = self._rhs.type_check()

        # Make sure both lhs and rhs are ints
        if(isinstance(lcheck, bool) or isinstance(rcheck, bool)):
            raise TypeCheckError("Error: Addition arguments are not of type S64.")
        elif(isinstance(lcheck, int) and isinstance(rcheck, int)):
            return 1;
        else:
            raise TypeCheckError("Error: Addition arguments are not of type S64.")

########################## Read #########################################################
# -- Inherited Class for Adding Numbers --

class read(expr):
    def __init__(self, num = 0, debug_mode = False):
        if debug_mode:
            self._num = int(num)
            self._debug_mode = True
        else:
            self._num = int(num)
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
        # Set purity to false since this program contains a read
        expr.purity = False

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

    def type_check(self):
        # Return an int so other type check tests know that read returns an int
        return 1;

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

    def type_check(self):
        # Check if self._x is accidently a var. If so, return to string.
        if(isinstance(self._x, var)):
            self._x = self._x._var

        # Immediately call Uniquify to avoid duplicate variables in env
        old_var = self._x
        self._x = uniquify(self._x, prog.type_env)
        self._xb.uniq(self._x, old_var)

        # Calculate xe, and add to enviroment so we can reference it's type later
        check_xe = self._xe.type_check()
        prog.type_env.add_var(self._x, check_xe)
        check_xb = self._xb.type_check()

        # Make sure xe and xb are of the same type, either bool or int
        if(isinstance(check_xe, bool) and isinstance(check_xb, bool)):
            return True;
        elif((isinstance(check_xe, bool) and isinstance(check_xb, int)) or (isinstance(check_xe, int) and isinstance(check_xb, bool))):
            raise TypeCheckError("Error: Let variable expression and variable body was not both of type bool or S64.")
        elif(isinstance(check_xe, int) and isinstance(check_xb, int)):
            return 1;
        else:
            raise TypeCheckError("Error: Let variable expression and variable body was not both of type bool or S64.")

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
        elif(isinstance(value, str)):
            return str(self._var) + "(" + str(value) + ")";
        else:
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

    def type_check(self):
        # Return the variables type
        return prog.type_env.find_var(self._var);


########################## Sub ##########################################################
class sub(expr):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + "-" + str(self._rhs.pretty_print()) + ")";

    # Use syntatic sugar - (+lhs (-rhs))
    def interp(self):
        result = add(self._lhs, neg(self._rhs))
        return result.interp()

    def type_check(self):
        lcheck = self._lhs.type_check()
        rcheck = self._rhs.type_check()

        # Make sure lhs and rhs are both ints
        if(isinstance(lcheck, bool) or isinstance(rcheck, bool)):
            raise TypeCheckError("Error: Subtraction arguments are not of type S64.")
        elif(isinstance(lcheck, int) and isinstance(rcheck, int)):
            return 1;
        else:
            raise TypeCheckError("Error: Subtraction arguments are not of type S64.")

    def opt(self):
        if(isinstance(self._lhs, read)):
            self._lhs = neg(self._lhs)

        if(isinstance(self._rhs, read)):
            self._rhs = neg(self._rhs)

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

            return add(left_opt, neg(right_opt));
        else:
            if (isinstance(right_opt, num) and (right_opt.opt() == 0)):
                return left_opt;

            if (isinstance(left_opt, num) and (left_opt.opt() == 0)):
                return right_opt;

            return ((left_opt) + (-1 * right_opt));

    def uniq(self, unique_var, old_var):
        # If either side is a let, then we do not want to go further since
        # we call uniq from let for each instance of a let
        if(type(self._lhs) is not let):
            self._lhs.uniq(unique_var, old_var)
        if(type(self._rhs) is not let):
            self._rhs.uniq(unique_var, old_var)
        return;

########################## If ###########################################################
class rif(expr):
    # c = condition, t = true side, f = false side
    def __init__(self, c, t, f):
        self._c = c
        self._t = t
        self._f = f

    def pretty_print(self):
        return "( if " + str(self._c.pretty_print()) + " then " + str(self._t.pretty_print()) + " else " +\
               str(self._f.pretty_print()) + ")";

    def interp(self):
        c_result = self._c.interp()
        t_result = self._t.interp()
        f_result = self._f.interp()

        if(c_result == True):
            return t_result;
        elif(c_result == False):
            return f_result;
        else:
            print("Error: If statement was neither true or false.")
            exit(1);

    def type_check(self, func_call = "If"):
        check = self._c.type_check()
        t_check = self._t.type_check()
        f_check = self._f.type_check()

        # Check first if condition is of type bool
        if(isinstance(check, bool)):
            # Check if true and false sections are either both int or bool
            if(isinstance(t_check, bool) and isinstance(f_check, bool)):
                return True;
            elif((isinstance(t_check, bool) and isinstance(f_check, int)) or (isinstance(t_check, int) and isinstance(f_check, bool))):
                raise TypeCheckError("Error: " + func_call + " True and False arguments were not both of type bool or int.")
            elif(isinstance(t_check, int) and isinstance(f_check, int)):
                return 1;
            else:
                raise TypeCheckError("Error: " + func_call + " True and False arguments were not both of type bool or int.")
        else:
            raise TypeCheckError("Error: " + func_call + " condition argument was not of type bool.")

    def opt(self):
        if ((isinstance(self._c, true)) or (isinstance(self._c, false))):
            opt_c = self._c
        else:
            opt_c = self._c.opt()

        opt_t = opt_helper(self._t)
        opt_f = opt_helper(self._f)

        if(opt_c is true()):
            # Set false condition to false, since we won't use it anyway
            opt_f = false()

        if(opt_c is false()):
            # Set true condition to false, since we won't be using it
            opt_t = false()

        # If condition is a not, reverse conditions
        if(isinstance(opt_c, rnot)):
            temp = opt_t
            opt_t = opt_f
            opt_f = temp
            opt_c = opt_c._arg

        return rif(opt_c, opt_t, opt_f);

    def uniq(self, unique_var, old_var):
        # If either side is a let, then we do not want to go further since
        # we call uniq from let for each instance of a let
        if(type(self._c) is not let):
            self._c.uniq(unique_var, old_var)
        if(type(self._t) is not let):
            self._t.uniq(unique_var, old_var)
        if(type(self._f) is not let):
            self._f.uniq(unique_var, old_var)
        return;

########################## Or ###########################################################
class ror(expr):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + " || " +  str(self._rhs.pretty_print()) + ")";

    def interp(self):
        return rif(self._lhs, true(), self._rhs).interp();

    def type_check(self):
        # Use if to check type
        check = rif(self._lhs, true(), self._rhs)
        result = check.type_check("Or")
        return result;

    def opt(self):
        lhs = self._lhs.opt()
        rhs = self._rhs.opt()

        if (lhs is True or rhs is True):
            return true()
        else:
            return false()

    def uniq(self, unique_var, old_var):
        # If either side is a let, then we do not want to go further since
        # we call uniq from let for each instance of a let
        if(type(self._lhs) is not let):
            self._lhs.uniq(unique_var, old_var)
        if(type(self._rhs) is not let):
            self._rhs.uniq(unique_var, old_var)
        return;


########################## And ##########################################################
class rand(expr):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + " && " +  str(self._rhs.pretty_print()) + ")";

    def interp(self):
        return rif(self._lhs, self._rhs, false()).interp()

    def type_check(self):
        # Use if to check type
        check = rif(self._lhs, self._rhs, false())
        result = check.type_check("And")
        return result;

    def opt(self):
        lhs = self._lhs.opt()
        rhs = self._rhs.opt()

        if (lhs is True and rhs is True):
            return true()
        else:
            return false()

    def uniq(self, unique_var, old_var):
        # If either side is a let, then we do not want to go further since
        # we call uniq from let for each instance of a let
        if(type(self._lhs) is not let):
            self._lhs.uniq(unique_var, old_var)
        if(type(self._rhs) is not let):
            self._rhs.uniq(unique_var, old_var)
        return;

########################## Not ##########################################################
class rnot(expr):
    def __init__(self, arg):
        self._arg = arg

    def pretty_print(self):
        return "(!" + str(self._arg.pretty_print()) + ")";

    # Not recommended to use syntatic sugar
    def interp(self):
        result = self._arg.interp()
        if(result == True):
            return False;
        elif(result == False):
            return True;
        else:
            print("Error: _not was neither true or false.")
            exit(1);

    def type_check(self):
        check = self._arg.type_check()

        # Check if arg is type bool
        if(isinstance(check, bool)):
            return True;
        else:
            raise TypeCheckError("Error: Not argument was not of type bool.")

    def opt(self):
        # Remove the nested not
        if(isinstance(self._arg, rnot)):
            # not(not(e)) = e
            self._arg = self._arg._arg

        return rnot(self._arg);

    def uniq(self, unique_var, old_var):
        self._arg.uniq(unique_var, old_var)
        return;

########################## Comparision ##################################################
class cmp(expr):
    def __init__(self, lhs, comp, rhs):
        self._lhs = lhs
        self._rhs = rhs
        # == | < | <= | > | >=
        self._comp = comp

    def pretty_print(self):
        return "(" + str(self._lhs.pretty_print()) + str(self._comp) + str(self._rhs.pretty_print()) + ")";

    def interp(self):
        lhs_result = self._lhs.interp()
        rhs_result = self._rhs.interp()

        if(self._comp == "=="):
            return lhs_result == rhs_result;
        elif(self._comp == "<"):
            return lhs_result < rhs_result;
        elif(self._comp == "<="):
            return lhs_result <= rhs_result;
        elif(self._comp == ">"):
            return lhs_result > rhs_result;
        elif(self._comp == ">="):
            return lhs_result >= rhs_result;
        else:
            print("Error: Relation Operator Not Found.")
            exit(1)

    def type_check(self):
        lcheck = self._lhs.type_check()
        rcheck = self._rhs.type_check()

        # Check if lhs and rhs are check
        if(isinstance(lcheck, bool) or isinstance(rcheck, bool)):
            raise TypeCheckError("Error: Comparision arguments are not of type S64.")
        if(isinstance(lcheck, int) and isinstance(rcheck, int)):
            return True;
        else:
            raise TypeCheckError("Error: Comparision arguments are not of type S64.")

    def opt(self):
        lhs = opt_helper(self._lhs)
        rhs = opt_helper(self._rhs)

        # Check if read is in program, and if each side is the equal
        if(expr.purity is True):
            if ((self._lhs == self._rhs) or (lhs == rhs)):
                if((self._comp is "==") or (self._comp is "<=") or (self._comp is ">=")):
                    return true()
                else:
                    # If equality is "<" or ">", then we know it must be false
                    return false()
            else:
                return cmp(lhs, self._comp, rhs).interp()
        return cmp(lhs, self._comp, rhs)

    def uniq(self, unique_var, old_var):
        # If either side is a let, then we do not want to go further since
        # we call uniq from let for each instance of a let
        if(type(self._lhs) is not let):
            self._lhs.uniq(unique_var, old_var)
        if(type(self._rhs) is not let):
            self._rhs.uniq(unique_var, old_var)
        return;

########################## Prog #########################################################
# -- Inherited Class for the Program "Container" --

class prog(expr):
    # Global variable that holds the linked list that maps var->num
    map_env = env()
    type_env = env()
    debugger = ""

    def __init__(self, info, e):
        self._info = info
        self._e = e
        self._type = None

    def interp(self):
        # Reinitialize Enviroment Mapping
        prog.map_env = env()

        # Reinitialize Type Mapping
        prog.type_env = env()

        # Copy program for type checking
        check = copy.deepcopy(self._e)

        # Type Check Program and save type for later
        self._type = check.type_check()

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

        # Index is used for optomization tests so that the default test has the same
        # random read values as the optomized test
        expr.opt_index = 0

        expr.arry_of_reads.clear()
        result = self._e.opt()

        expr.neg_count = 0
        generate = num(result)

        # Insert a read into the program based on if the read was intended to be negative or not
        for reads in expr.arry_of_reads:
            if (reads == -1):
                if (isinstance(generate, int)) and (generate == 0):
                    generate = neg(read())
                else:
                    generate = add(neg(read()), generate)
            elif (reads == 1):
                if (isinstance(generate, int)) and (generate == 0):
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
