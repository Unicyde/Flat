import sys
from utils import *
from lexer import lex
from preprocessor import process

builtins = ["print", "input"]

defs = {}

vars = {}



def evaluate(toks):
    i = 0
    expr = ""
    string = -1
    while i < len(toks):
        t = toks[i]
        if tokType(t) == "NUM":
            s = t[4:]
            
            if string == -1:
                string = 0
            elif string == 1:
                raise TypeError("Invalid type {0}, expecting a string!".format(tokType(val)))
            
            expr += s
        
        elif tokType(t) == "SYM":
            if len(toks) > i+1 and toks[i+1] == "COLON":
                print("Function")
            else:
                if t[4:] not in vars:
                    raise NameError("Invalid pointer {0}!".format(t[4:]))
                
                val = vars[t[4:]]
                
                if tokType(val) == "NUM":
                    if string == -1:
                        string = 0
                    elif string == 1:
                        raise TypeError("Invalid type {0}, expecting a string!".format(tokType(val)))
                    
                    if len(toks) > i+1 and toks[i+1][-1] == "*":
                        if len(toks) > i+2 and tokType(toks[i+2]) == "STR":
                            s = toks[i+2][4:]
                            
                            times = 0
                            r = val[4:]
                            
                            try:
                                times = eval(r)
                            except:
                                raise SyntaxError("Can't evaluate {0}!".format(r))
                            
                            s = times * s
                            expr += s
                            
                            string = 1
                            
                            i += 3
                            continue
                    
                    expr += val[4:]
                
                elif tokType(val) == "STR":
                    s = val[4:]
                    
                    if string == -1:
                        string = 1
                    elif string == 0:
                        raise TypeError("Invalid type {0}, expecting a number!".format(tokType(t)))
                    
                    if len(toks) > i+1 and toks[i+1][0:5] == "NUM:*":
                        r = toks[i+1][5:]
                        times = 0
                        
                        try:
                            times = eval(r)
                        except:
                            raise SyntaxError("Can't evaluate {0}!".format(r))
                        
                        s = s * int(times)
                    
                    expr += s
                    
                    if len(toks) > i+1 and toks[i+1][4:] == "+":
                        i += 1
        
        elif tokType(t) == "STR":
            s = t[4:]
            
            if string == -1:
                string = 1
            elif string == 0:
                raise TypeError("Invalid type {0}, expecting a number!".format(tokType(t)))
            
            if len(toks) > i+1 and toks[i+1][0:5] == "NUM:*":
                r = toks[i+1][5:]
                times = 0
                
                try:
                    times = eval(r)
                except:
                    raise SyntaxError("Can't evaluate {0}!".format(r))
                
                s = s * int(times)
            
            expr += s
            
            i += 1
            
        else:
            raise TypeError("Invalid type {0}, expecting a number!".format(tokType(t)))
        
        i += 1
    
    if string == 1 or expr == "":
        return "STR:" + parseString(expr)
    else:
        try:
            return "NUM:" + str(eval(strip(expr)))
        except:
            return "NUM:" + strip(expr)
            #raise SyntaxError("Can't evaluate {0}!".format(expr))

# Inner functions

def assign(name, value):
    vars[name] = value

def builtin(name, args):
    if name == "print":
        print("".join(args))
    elif name == "input":
        if len(args) == 1:
            """ Core input """
            
            usrIn = input(args[0])
            
            if isNum(usrIn):
                usrIn = "NUM:" + usrIn
            else:
                usrIn = "STR:" + usrIn
            
            return usrIn
        
        else:
            raise IndexError("Invalid argument length {0}, 1 expected!".format(len(args)))
    else:
        raise NameError("Invalid pointer '{0}'!".format(name))

def function(name, args):
    if name in builtins:
        return builtin(name, args)

    elif name in defs:
        print("Function!")

    else:
        raise NameError("Invalid pointer '{0}'!".format(name))

def parseString(string):
    out = ""
    name = ""
    load = 0
    for c in string:
        if c == "{":
            if load == 1:
                raise NameError("Variable names can't contain '{'!")
            load = 1
        elif c == "}":
            if load == 0:
                raise SyntaxError("Closing unstarted block!")
            load = 0
            if name not in vars:
                raise NameError("Invalid pointer {0}!".format(name))
            out += vars[name][4:]
            name = ""
        elif load == 1:
            name += c
        else:
            out += c
    return out




### Argument parser ###

def getArgs(params, t=""):
    args = []

    comma = 0

    i = 0
    while i < len(params):
        if comma == 1:
            if params[i] == "COMMA":
                comma = 0
                i += 1
                continue
            else:
                raise SyntaxError("Expecting a comma!")

        if tokType(params[i]) == "NUM":
            val = ""
            
            r = getUnless(params, "COMMA", i)
            
            args.append(evaluate(r)[4:])
            i = getUnlessIndex(params, "COMMA", i)
            comma = 1
            continue
        
        elif tokType(params[i]) == "SYM":
            if len(params) > i+1 and params[i+1] == "COLON":
                """ Function call """
                
                a = getArgs(getUnless(params, "SEMI", i+2))
                name = params[i][4:]
                
                r = function(name, a)
                i = getUnlessIndex(params, "SEMI", i+2)
                
                if len(params) > i and tokType(params[i]):
                    expr = getUnless(params, "COMMA", i)
                    expr.insert(0, r)
                    
                    i = getUnlessIndex(params, "COMMA", i)
                    
                    r = "NUM:" + evaluate(expr)
                
                args.append(r[4:])
                i -= 1
            else:
                if params[i][4:] not in vars:
                    raise NameError("Invalid pointer {0}!".format(params[i][4:]))
                
                r = getUnless(params, "COMMA", i)
                
                if len(r) > 1:
                    r = getArgs(addAll(r, "COMMA"))
                    r = generateType(r)
                    r = process(r)
                else:
                    args.append(vars[params[i][4:]][4:])
                    comma = 1
                    i += 1
                    continue
                
                args.append(evaluate(r))
                i = getUnlessIndex(params, "COMMA", i)
                comma = 1
                continue
        
        elif tokType(params[i]) == "STR":
            s = params[i][4:]
            
            if len(params) > i+1 and params[i+1][4] == "*":
                r = getUnless(params, "COMMA", i+1)
                i = getUnlessIndex(params, "COMMA", i+1)
                
                expr = getArgs(r)[0]
                
                try:
                    j = round(eval(expr[1:]))
                except:
                    raise SyntaxError("Can't count {0}!".format(expr[1:]))
                
                if j > sys.maxsize:
                    raise OverflowError("Maximal integer is {0}, found {1}!".format(sys.maxsize, j))
                
                s = s * int(j)
            
            args.append(parseString(s))
            

        comma = 1

        i += 1
    
    return args




### Parsing function ###

def parse(toks):
    i = 0
    while i < len(toks):
        if tokType(toks[i]) == "SYM":
            name = toks[i][4:]

            if toks[i+1] == "COLON":
                r = getUnless(toks, "NEWLN", i+2)
                i = getUnlessIndex(toks, "NEWLN", i+2)
                
                args = getArgs(r)
                function(name, args)

            elif toks[i+1] == "EQ":
                r = getUnless(toks, "NEWLN", i+2)
                i = getUnlessIndex(toks, "NEWLN", i+2)
                
                expr = getArgs(r)
                expr = generateType(expr)
                expr = process(expr)
                
                val = evaluate(expr)
                
                assign(name, val)
            
            elif toks[i+1] == "APPEND" or toks[i+1] == "DEAPPEND":
                if name not in vars:
                    raise NameError("You need to declare variable before you try to append!")
                
                if tokType(vars[name]) == "NUM":
                    """ Number increase """
                    
                    mode = toks[i+1]
                    
                    expr = ""
                    r = getArgs(getUnless(toks, "NEWLN", i+2))
                    i = getUnlessIndex(toks, "NEWLN", i+2) - 2
                    
                    for o in r:
                        expr += o
                    
                    if mode == "APPEND":
                        vars[name] = "NUM:" + splitNum(str(eval(strip(vars[name][4:]) + "+" + strip(expr))))
                    else:
                        vars[name] = "NUM:" + splitNum(str(eval(strip(vars[name][4:]) + "-" + strip(expr))))
                    i += 2
                
                elif tokType(vars[name]) == "STR":
                    """ String append """
                    
                    if toks[i+1] == "APPEND":
                        expr = ""
                        r = getArgs(getUnless(toks, "NEWLN", i+2))
                        i = getUnlessIndex(toks, "NEWLN", i+2)
                        
                        for o in r:
                            expr += o
                        
                        vars[name] += expr
                    else:
                        """ Next should be number used to remove indexes from string """
                        
                        expr = ""
                        r = int(getArgs(getUnless(toks, "NEWLN", i+2), "NUM")[0])
                        i = getUnlessIndex(toks, "NEWLN", i+2)
                        
                        if r >= len(vars[name][4:]):
                            ln = len(vars[name][4:])
                            raise IndexError("Index {0} is greater than length {1}!".format(r, ln))
                        
                        vars[name] = "STR:" + vars[name][4:-r]
                
                else:
                    raise TypeError("Invalid type {0}, expecting number or string!".format(tokType(vars[name])))

            else:
                raise SyntaxError("Unexpected token {0} - expecting a '=' or ':'!".format(toks[i+1]))

        elif toks[i] == "NEWLN":
            pass

        else:
            raise SyntaxError("Unexpected token {0}!".format(toks[i]))

        i += 1