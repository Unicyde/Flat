from utils import *

def process(toks, minimal=0):
    i = 0
    while i < len(toks):
        if tokType(toks[i]) == "NUM":
            toks[i] = toks[i].replace("^", "**")
            
            if toks[i][4:] == "+":
                if len(toks) > i+1 and toks[i+1] == "EQ":
                    toks[i] = "APPEND"
                    del toks[i+1]
                    continue
            elif toks[i][4:] == "-":
                if len(toks) > i+1 and toks[i+1] == "EQ":
                    toks[i] = "DEAPPEND"
                    del toks[i+1]
                    continue
            elif toks[i][4:] == "e" and tokType(toks[i+1]) == "SYM":
                toks[i] = "SYM:e" + toks[i+1][4:]
                del toks[i+1]
                if toks[i][4:] in tokenSpec:
                    toks[i] = tokenSpec[toks[i][4:]]
                continue
            
            toks[i] = "NUM:" + strip(toks[i][4:])
                
            try:
                toks[i] = "NUM:" + str(eval(toks[i][4:]))
                
                if minimal == 0:
                    toks[i] = "NUM:" + splitNum(toks[i][4:])
            except Exception as e:
                """ Parser will care about this """
                
                pass
            
            if toks[i][4:] == "--" or toks[i][4:] == "---":
                del toks[i:getUnlessIndex(toks, "NEWLN", i)]
            
            if len(toks) > i+1 and tokType(toks[i+1]) == "NUM":
                if toks[i+1][4:] == "--" or toks[i+1][4:] == "---":
                    i += 1
                    continue
                
                toks[i] += toks[i+1][4:]
                
                del toks[i+1]
                continue
        
        elif tokType(toks[i]) == "STR":
            if len(toks) > i+1 and toks[i+1] == "NUM:+":
                if len(toks) > i+2 and tokType(toks[i+2]) == "STR":
                    toks[i] += toks[i+2][4:]
                    
                    del toks[i+1]
                    del toks[i+1]
                    continue
                
                elif tokType(toks[i+2]) == "SYM":
                    """ It will be evaluated in runtime """
                else:
                    raise TypeError("String and {0} can't be appended!".format(tokType(toks[i+2])))
        
        elif toks[i] == "GT" or toks[i] == "LT":
            if len(toks) > i+1 and toks[i+1] == "EQ":
                del toks[i+1]
                toks[i] = toks[i] + "EQ"
                continue
        
        elif toks[i] == "ELIF":
            toks[i] = "ELSE"
            toks.insert(i+1, "IF")
            continue
        
        i += 1
    
    return toks