from sys import *

import lexer
from preprocessor import process
from parser import parse
from utils import *

def main():
    if len(argv) == 1:
        raise IndexError("Please, give me a source file or type a command.")
    elif len(argv) == 2:
        raise IndexError("You need to specify amount of spaces used for indentation!")
    else:
        if not isNum(argv[2]):
            raise TypeError("Amount of spaces can be only number!")
        if argv[2][0] != "-":
            raise SyntaxError("Syntax for flags is: '-[flagname]', found: %s!" % argv[2])
        lexer.spaceCount = int(argv[2][1:])
    
    src = open(argv[1], "r").read()
    src = replaceEscapes(src)

    data = lexer.lex(src)
    data = [replaceEscapes(d) for d in data]
    
    data = process(data)
    data = [replaceEscapes(d) for d in data]
    
    parse(data)

main()