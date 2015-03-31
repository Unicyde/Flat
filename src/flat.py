from sys import *

from lexer import lex
from preprocessor import process
from parser import parse
from utils import *

def main():
    if len(argv) == 1:
        print("Please, give me a source file or type a command.")
    
    src = open(argv[1], "r").read()
    src = replaceEscapes(src)
    
    minimal = 0
    if len(argv) > 2 and argv[2] == "-min":
        minimal = 1

    data = lex(src)
    data = [replaceEscapes(d) for d in data]
    
    data = process(data, minimal)
    data = [replaceEscapes(d) for d in data]
    
    # print(data)

    parse(data)

main()