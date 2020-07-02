
# Sintaxis:

"""
# var deffinition:
var: predicat int name
var float name

# set var value
set: var value

# add rule
rule: name value <= a = "b", c < "d", list << 5
"""

def define_comparator(comp):
    if comp == "==":
        return lambda x, y: x == y
    if comp == ">":
        return lambda x, y: x > y
    if comp == "<":
        return lambda x, y: x < y
    if comp == "!=":
        return lambda x, y: x != y # and x != None

def define_value(target, second):
    if target.type == "bool":
        if second == "True":
            return True
        elif second == "False":
            return False
        else:
            raise TypeError("Not a bool value")
    elif target.type == "str":
        if second[0] == second[-1] == "\"":
            return second[1:-1]
    elif target.type == "float":
        try:
            return float(second)
        except ValueError:
            raise TypeError("Not a float")
    elif target.type == "int":
        if not second.isdigit():
            raise TypeError("Not a int value")
        return int(second)
        



# Shell has main storage of variables from compilefile
# and temp storage with compute data and user data

class SystemShell:
    def __init__(self):
        self.graph = {}
        self.temp_storage = {}
        self.history = None
        self.askable = []
    # compile file read lines of file and create new variables with values and rules
    def compile_file(self, filename):
        with open(filename, "r") as fd:
            for line in fd:
                words = line[:-1].split(": ")
                if not words[0]:
                    continue
                if words[0] == 'rule':
                    self.add_rule(words[1])
                vs =  words[1].split()
                if words[0] == 'var':
                    self.add_var(vs)
                if words[0] == 'set':
                    self.add_set(vs)

    def get_value(self, varname):
        self.history = None
        if varname not in self.graph:
            raise ValueError("Undefined var name")
        res = self.graph[varname].get_value()
        self.history = self.graph[varname].get_history()
        return res
    
    def get_last_history(self):
        return self.history

    def get_vars(self):
        return dict(self.graph)

    def clear_storage(self):
        self.temp_storage.clear()

    def get_temp_storage(self):
        return dict(self.temp_storage)

    def set_value(self, varname, value):
        if varname not in self.graph:
            raise ValueError("Undefined var name")
        if self.graph[varname].predict:
            self.temp_storage[varname].append(value)
        else:
            if not self.graph[varname].value is None:
                raise ValueError("This variable has setted value")
            self.temp_storage[varname] = value

    def get_askable(self):
        return list(self.askable)
                    

    def add_var(self, vs):
        i = 0
        predict = False
        if vs[0] == 'predicat':
            predict = True
            i += 1
        self.graph[vs[i + 1]] = Variable(self, vs[i + 1], vs[i], predict)
        if len(vs) > i + 2 and vs[i + 2] == "askable":
            self.askable.append((vs[i + 1], vs[i]))

    def add_set(self, vs):
        target = self.graph[vs[0]]
        if target.predict:
            if target.type == "bool":
                raise TypeError("Bool not be in predicat")
            else:
                target.value.append(define_value(target, vs[1]))
        else:
            target.value = define_value(target, vs[1])

    # rule: target val <= vs
    def add_rule(self, vs):           
        rule = vs.split(" <= ")
        target = self.graph[rule[0].split()[0]]
        val = define_value(target, rule[0].split()[1])
        if val not in target.rules:
            target.rules[val] = []
        target.rules[val].append(Rule(self, rule[1]))


# compare with value
class SimpleCompare:
    def __init__(self, shell, var, comparator, value):
        self.shell = shell
        self.var = var
        self.value = value
        self.comparator = comparator
        self.compare = define_comparator(comparator)
        self.history = {}

    def result(self):
        self.history = {}
        if self.var.predict:
            if not self.compare is None:
                raise TypeError("Predicat may be compared only")
            res = self.var.check_value(self.value)
            self.history[(self.var.name, self.comparator, self.value)] = dict(self.var.get_history())
            return res
        val = self.var.get_value()
        if val is None and self.var.type != "bool":
            return False
        self.history[(self.var.name, self.comparator, self.value)] = dict(self.var.get_history())
        return self.compare(val, self.value)

    def get_history(self):
        return self.history

    
    def __repr__(self):
        return str(self.var.name, self.comparator, self.value)


#compare with var
class HardCompare:
    def __init__(self, shell, var1, comparator, var2):
        self.shell = shell
        self.var1 = var1
        self.var2 = var2
        self.comparator = comparator
        self.compare = define_comparator(comparator)  
        self.history = {} 

    def result(self):
        self.history = {}
        if self.var1.type != self.var2.type:
            raise TypeError("Comparation with diffrent")
        if self.var1.predict or self.var2.predict or self.comparator == "<<":
            raise TypeError("Wrong args for hard compare")     
        val1 = self.var1.get_value()
        val2 = self.var2.get_value()
        if val1 is None or val2 is None:
            return False
        self.history[(self.var1.name, self.comparator, self.var2.name)] = dict(self.var1.get_history())
        self.history[(self.var1.name, self.comparator, self.var2.name)].update(self.var1.get_history())
        return self.compare(val1, val2)

    def get_history(self):
        return self.history
    
    def __repr__(self):
        return str(self.var1.name, self.comparator, self.var2.name)
        



class Rule:
    def __init__(self, shell, rule):
        self.shell = shell
        self.compares = []
        self.history = {}
        compares = rule.split(", ")
        for comp in compares:
            first, comp, second = tuple(comp.split())
            target = shell.graph[first]
            value = define_value(target, second)
            if value is None:
                if second not in shell.graph:
                    raise TypeError("Unknown value of comparation")
                else:
                    self.compares.append(HardCompare(shell, target, comp, shell.graph[second]))
            else:
                self.compares.append(SimpleCompare(shell, target, comp, value))

    def complete(self):
        self.history = {}
        for compar in self.compares:
            if not compar.result():
                return False
            self.history.update(compar.get_history())
        return True

    def get_history(self):
        return self.history
    
    def __repr__(self):
        return self.compares
                
            
      


class Variable:
    def __init__(self, shell, name, type, predict):
        self.name = name
        self.shell = shell
        self.type = type
        self.value = None
        self.rules = {}
        self.predict = predict
        self.history = {}
        if predict:
            self.value = []
            self.shell.temp_storage[name] = []

    def get_value(self):
        if not self.predict:
            if self.name in self.shell.temp_storage:
                #self.history[(self.name, "=", self.shell.temp_storage[self.name])] = {}
                return self.shell.temp_storage[self.name]
            self.history = {}
            if not self.value is None:
                self.history[(self.name, "=", self.value)] = {}
                return self.value
            for key in self.rules:
                for rule in self.rules[key]:
                    if rule.complete():
                        self.history[(self.name, "=", key)] = dict(rule.get_history())
                        self.shell.temp_storage[self.name] = key
                        return key
            return None
        else:
            raise TypeError("Predicat may be checked only")

    def check_value(self, val):
        if self.predict:
            if val in self.value or val in self.shell.temp_storage[self.name]:
                self.history[(self.name, "<<", val)] = {}
                return True
            if val not in self.rules:
                return False
            for rule in self.rules[val]:
                if rule.complete():
                    self.history[(self.name, "<<", val)] = dict(rule.get_history())
                    self.shell.temp_storage[self.name].append(val)
                    return True
            return False
        else:
            raise TypeError("Only predicat may be checked")
    
    def get_history(self):
        return self.history

    def __repr__(self):
        return str((self.name, self.value))
