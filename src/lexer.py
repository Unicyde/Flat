from utils import *

tokens = []
indent = 0

def countIndent(line):
    global indent
    global tokens

    ind = len(line) - len(line.lstrip("\t"))

    if ind != indent:
        if ind > indent:
            while ind - indent != 0:
                indent += 1
                tokens.append("INDENT")

        elif ind < indent:
            while indent - ind != 0:
                indent -= 1
                tokens.append("DEDENT")

def lex(data):
    data = splitByNewline(data)

    global tokens
    global indent

    tok = ""

    isstr = False
    string = ""

    num = ""

    for line in data:
        i = 0
        while i < len(line):
            c = line[i]

            if isSpecial(c) and tok != "":
                tokens.append("SYM:" + tok)
                tok = ""

            tok += c

            if not isMath(tok) and tok != "." and num != "" and tok != " ":
                tokens.append("NUM:" + num)
                num = ""

            countIndent(line)

            if tok == "\"":
                isstr = not isstr

                if not isstr:
                    tokens.append("STR:" + string)
                    string = ""

                tok = ""

            elif isstr:
                if tok == "\\":
                    tok += line[i+1]
                    i += 1

                string += tok
                tok = ""

            elif isMath(tok) or ((tok == "." or tok == " ") and num != ""):
                if tok == " " and len(line) > i+1 and not isMath(line[i+1]):
                    tokens.append("NUM:" + num)
                    num = ""
                else:
                    num += tok
                tok = ""

            elif tok == " " or tok == "\n" or tok == "\t":
                tok = ""

            elif tok in tokenSpec:
                tokens.append(tokenSpec[tok])
                tok = ""

            i += 1
        if num != "":
            tokens.append("NUM:" + num)
            num = ""
        if tok != "":
            tokens.append("SYM:" + tok)
            tok = ""

        tokens.append("NEWLN")
        tok = ""

    if tok != "":
        tokens.append("SYM:" + tok)

    if indent > 0:
        while indent != 0:
            indent -= 1
            tokens.append("DEDENT")

    return tokens