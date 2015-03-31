import re
from sys import *

tokenSpec = {":": "COLON", ";": "SEMI", "=": "EQ", "<": "LT", ">": "GT", ",": "COMMA"}

literals = ["STR", "NUM", "BOOL"]

def addAll(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def replaceEscapes(string):
    return string.replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t").replace('\\\\"', '"')

def splitByNewline(string):
    toks = []
    line = ""
    esc = False
    s = False
    for c in string:
        if c == "\"":
            if not esc:
                s = not s
            else:
                esc = False
        elif c == "\\":
            esc = not esc
        elif c == "\n" and not s:
            toks.append(line)
            line = ""
            continue
        line += c
    if line != "":
        toks.append(line)
    return toks



def generateType(string):
    if type(string) is list:
        return [generateType(x) for x in string]
    else:
        if tokType(string):
            return string
        else:
            if isNum(string):
                return "NUM:" + string
            else:
                return "STR:" + string

def tokType(token):
    if type(token) is str:
        if ":" in token:
            out = ""
            for c in token:
                if c == ":":
                    break
                out += c
            return out
        else:
            return None
    elif type(token) is list:
        for i, t in enumerate(token):
            if i != 0 and tokType(t) != tokType(token[i-1]):
                return "multi"
        return tokType(token[0])
    else:
        raise TypeError("Unsupported type {0}, expecting List or String!".format(type(token)))


def strip(num):
    return re.sub(" +", "", num)

def splitNum(num):
    num = list(num)
    
    i = 0
    for c in num:
        if c == ".":
            break
        i += 1
    
    if i > 3:
        ii = 0
        while i != 0:
            i -= 1
            ii += 1
            
            if ii % 3 == 0 and i != 0:
                num.insert(i, " ")
    
    return "".join(num)


# Parser functions

def getUnless(toks, stop, start=0):
    i = start
    out = []

    if i >= len(toks):
        raise IndexError("List index out of range - %i, max %i!" % i, len(toks))

    while i < len(toks) and toks[i] != stop:
        out.append(toks[i])
        i += 1

    return out

def getUnlessIndex(toks, stop, start=0):
    i = start
    
    if i >= len(toks):
        raise IndexError("List index out of range - %i, max %i!" % i, len(toks))
    
    while i < len(toks) and toks[i] != stop:
        i += 1
    
    return i


# Checkers

def isNum(char):
    try:
        d = eval(char) + 1
        return True
    except:
        for c in char:
            if not isMathOp(c) and c not in ["0","1","2","3","4","5","6","7","8","9",".","e"]:
                return False
        return True

def isWhite(char):
    return char == " " or char == "" or char == "\t" or char == "\r" or char == "\n"

def isLogical(char):
    return char == "=" or char == "<" or char == ">"

def isMathOp(char):
    return char == "+" or char == "-" or char == "*" or char == "/" or char == "^"

def isMath(char):
    return isMathOp(char) or isNum(char) or char == "(" or char == ")"

def isOperator(char):
    return char == ":" or char == ";" or char == "." or char == "," or isLogical(char) or isMathOp(char)

def isBrace(char):
    return char == "(" or char == ")" or char == "[" or char == "]" or char == "{" or char == "}"

def isSpecial(char):
    return isWhite(char) or isOperator(char) or isBrace(char)