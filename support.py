#
#	Nick Quinn - Compiler Construction
#
#   This file contains support functions and classes that are commonly
#   used in the C, X, and R languages.

### Support Classes ###

########################## Node #########################################################
# -- Node Class for Linked List in Env (Enviroment) --

class TypeCheckError(Exception):
	pass

########################## Node #########################################################
# -- Node Class for Linked List in Env (Enviroment) --

class node():
	def __init__(self, var, num):
		self._var = var
		self._num = num
		self.next = None

########################## Env ##########################################################
# -- Class env (enviroment) --

class env():
	def __init__(self):
		self._head = None

	def find_var(self, var):
		temp = self._head
		while temp != None:
			if (temp._var == var):
				return temp._num;
			temp = temp.next;
		#print (" No mapping found. ")
		return None;

	def add_var(self, var, x):
		new_node = node(var, x)
		if (self._head == None):
			self._head = new_node
		else:
			temp = self._head
			new_node.next = temp
			self._head = new_node

########################## Uniquify #####################################################
# -- Looks for the var passed in the enviroment, and creates a new unique var if it already
# -- exists
def uniquify(var, enviroment):
	unique_count = 1
	temp = enviroment.find_var(var)
	new_var = var
	while(temp != None):
		new_var = var + str(unique_count)
		temp = enviroment.find_var(new_var)
		unique_count += 1

	return new_var;

########################## Create Unique Var ############################################
# -- Creates a new unique variable based of the enviroment. These variables are distinguished
# -- because they start with "_u"
def create_unique_var(enviroment):
	default_var = "_u"
	unique_var = uniquify(default_var, enviroment)
	return unique_var;
