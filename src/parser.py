import sys
import ast

from utils import *
from lexer import lex
from booleans import *
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



# Boolean condition parser

def condition(cond):
    final = []
    a = ""
    b = ""
    o = ""
    i = 0
    while i < len(cond):
        if tokType(cond[i]):
            a = cond[i]
            if len(cond) > i+1 and cond[i+1] in operators:
                o = cond[i+1]
                if len(cond) > i+2 and tokType(cond[i+2]):
                    b = cond[i+2]
                    
                    if o == "EQ":
                        final.append(str(a == b))
                    elif o == "LT":
                        if tokType(a) != "NUM" or tokType(b) != "NUM":
                            raise TypeError("Can't apply integer operator to %s and %s!" % (tokType(a), tokType(b)))
                        final.append(str(float(a[4:]) < float(b[4:])))
                    elif o == "GT":
                        if tokType(a) != "NUM" or tokType(b) != "NUM":
                            raise TypeError("Can't apply integer operator to %s and %s!" % (tokType(a), tokType(b)))
                        final.append(str(float(a[4:]) > float(b[4:])))
                    elif o == "LTEQ":
                        if tokType(a) != "NUM" or tokType(b) != "NUM":
                            raise TypeError("Can't apply integer operator to %s and %s!" % (tokType(a), tokType(b)))
                        final.append(str(float(a[4:]) <= float(b[4:])))
                    elif o == "GTEQ":
                        if tokType(a) != "NUM" or tokType(b) != "NUM":
                            raise TypeError("Can't apply integer operator to %s and %s!" % (tokType(a), tokType(b)))
                        final.append(str(float(a[4:]) >= float(b[4:])))
                    elif o == "NOTEQ":
                        final.append(str(a != b))
        elif cond[i] in ["AND", "OR"]:
            final.append(cond[i])
        
        i += 1
    
    if len(final) == 1:
        return final[0]
    else:
        return bool_eval(generateString(final))



# Inner functions

def slicer(r, i, s, o=0):
    if "COLON" not in r:
        r1 = getUnless(r, "RS", i)
        i = len(r)
        
        if o == 1:
            return i
        
        i1 = evaluate(r1)
        
        if tokType(s) == "STR":
            s = s[4:]
            if tokType(i1) != "NUM":
                raise TypeError("Strings can be only sliced by numbers, found %s!" % tokType(i1))
            i1 = int(i1[4:])
            if i1 >= len(s):
                raise IndexError("Maximal index is %i, found %i!" % (len(s)-1, i1))
            
            return s[i1]
        elif tokType(s) == "NUM":
            s = s[4:]
            i1 = int(i1[4:])
            if i1 % 10 != 0:
                raise ValueError("Numbers can be only sliced by power of 10, found %i!" % i1)
            return s[-(str(i1).count("0"))]
    else:
        r1 = getUnless(r, "COLON", i)
        i = getUnlessIndex(r, "COLON", i)
        r2 = getUnless(r, "RS", i+1)
        i = getUnlessIndex(r, "RS", i+1)
        
        if o == 1:
            return i
        
        i1 = evaluate(r1)
        i2 = evaluate(r2)
        
        if tokType(s) == "STR":
            s = s[4:]
            if i1[4:] == "":
                i1 = "NUM:0"
            
            if tokType(i1) != "NUM":
                raise TypeError("Strings can be sliced by numbers, found %s!" % tokType(i1))
            elif i2[4:] == "":
                return s[int(i1[4:]):]
            elif tokType(i2) != "NUM":
                raise TypeError("Strings can be sliced by numbers, found %s!" % tokType(i2))
            else:
                return s[int(i1[4:]):int(i2[4:])]
        elif tokType(s) == "NUM":
            s = s[4:]
            
            if i1[4:] != "" and int(i1[4:]) % 10 != 0:
                raise ValueError("Numbers can be only sliced by power of 10, found %s!" % i1[4:])
            
            if i1[4:] != "" and tokType(i1) != "NUM":
                raise TypeError("Numbers can be sliced by numbers, found %s!" % tokType(i1))
            elif i2[4:] == "":
                return s[-(i1[4:].count("0")):]
            elif tokType(i2) != "NUM":
                raise TypeError("Numbers can be sliced by numbers, found %s!" % tokType(i2))
            
            return s[-(i1[4:].count("0")):-(i2[4:].count("0"))]

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
            if len(params) > i+1 and params[i+1] == "LS":
                s = params[i]
                bak = i
                
                r = generateType(slicer(params, i+2, s))
                i = slicer(params, i+2, s, 1)
                
                del params[bak:i+1]
                i = bak
                params.insert(i, r)
                continue
            else:
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
                
                bak = i
                i = getUnlessIndex(params, "SEMI", i+2)
                
                if len(params) > i and tokType(params[i]):
                    expr = getUnless(params, "COMMA", i)
                    expr.insert(0, r)
                    
                    i = getUnlessIndex(params, "COMMA", i)
                    
                    r = "NUM:" + evaluate(expr)
                
                del params[bak:i+1]
                params.insert(bak, r)
                i = bak
                continue
            else:
                if params[i][4:] not in vars:
                    raise NameError("Invalid pointer {0}!".format(params[i][4:]))
                if len(params) > i+1 and params[i+1] == "LS":
                    s = vars[params[i][4:]]
                    
                    if tokType(s) != "STR" and tokType(s) != "NUM":
                        raise TypeError("Only strings and numbers can be sliced, found %s!" % tokType(s))
                    
                    bak = i
                    
                    r = slicer(params, i+2, s)
                    i = slicer(params, i+2, s, 1)
                    
                    del params[bak:i+1]
                    i = bak
                    params.insert(i, r)
                    continue
                else:
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
            s = params[i]
            
            if len(params) > i+1 and params[i+1] == "LS":
                bak = i
                
                r = generateType(slicer(params, i+2, s))
                i = slicer(params, i+2, s, 1)
                
                del params[bak:i+1]
                i = bak
                params.insert(i, r)
                continue
            
            elif len(params) > i+1 and params[i+1][4] == "*":
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
            
            args.append(parseString(s[4:]))
        else:
            args.append(params[i])
            

        comma = 1

        i += 1
    
    return args




### Parsing function ###

def parse(toks):
    indent = []
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
                        vars[name] = "NUM:" + str(eval(strip(vars[name][4:]) + "+" + strip(expr)))
                    else:
                        vars[name] = "NUM:" + str(eval(strip(vars[name][4:]) + "-" + strip(expr)))
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
        
        elif toks[i] == "IF":
            r = getUnless(toks, "NEWLN", i)
            i = getUnlessIndex(toks, "NEWLN", i) + 2
            
            if r[-1] != "COLON":
                raise SyntaxError("Syntax for 'if' is: 'if condition:'!")
            
            cond = r[1:-1]
            cond = generateType(getArgs(addAll(cond, "COMMA")))
            b = toBool(condition(cond))
            
            if b:
                indent.insert(0, 1)
            else:
                bl = 1
                while bl != 0:
                    if toks[i] == "INDENT":
                        bl += 1
                    elif toks[i] == "DEDENT":
                        bl -= 1
                    i += 1
                indent.insert(0, 0)
            i -= 1
        
        elif toks[i] == "ELSE":
            if len(indent) == 0:
                raise SyntaxError("Else without if!")
            elif indent[0] == 1:
                if len(toks) > i+1 and toks[i+1] != "COLON" and toks[i+1] != "IF":
                    raise SyntaxError("Expecting ':' after 'else'!")
                
                bl = 1
                i += 4
                
                while bl != 0:
                    if toks[i] == "INDENT":
                        bl += 1
                    elif toks[i] == "DEDENT":
                        bl -= 1
                    i += 1
                
                del indent[0]
                i -= 2
            else:
                if len(toks) > i+1 and toks[i+1] == "COLON":
                    i += 1
                    del indent[0]
                elif len(toks) > i+1 and toks[i+1] == "IF":
                    del indent[0]
                else:
                    raise SyntaxError("Expecting ':' after 'else'!")
        
        elif toks[i] == "INDENT":
            if len(indent) > 0 and indent[0] == -1:
                raise SyntaxError("Unexpected indent!")
        
        elif toks[i] == "DEDENT":
            pass

        elif toks[i] == "NEWLN":
            pass

        else:
            raise SyntaxError("Unexpected token {0}!".format(toks[i]))

        i += 1