from pentadClass import pentadStruct
from LexicalAnalyser import spaceNormalizer
import re

def findS1(listOfEveryPentads = None, criterionVariable = "a", criterionLine = 10):
    i = 0
    for i in range (len(listOfEveryPentads)):
        listOfEveryPentads[i].text = ' ' + listOfEveryPentads[i].text #for lines that start directly with "for"
        pattern = re.compile(r'(?P<first>\W|\0|^)for\s*(?P<second>(\(|\\|\0|$))')
        if(re.search(pattern, listOfEveryPentads[i].text)):
            found = re.search(pattern, listOfEveryPentads[i].text)
            #print("FOR printing --> ", "first = ", found.group('first'), " second = ", found.group('second'))
            #print("FOR printing --> ", "before = ", listOfEveryPentads[i].text)
            listOfEveryPentads[i].text = re.sub(pattern, found.group('first') + " " + found.group('second'), listOfEveryPentads[i].text)
            #print("FOR printing --> ", "after = ", listOfEveryPentads[i].text)
            condition = varDecChangedToInt(listOfEveryPentads[i].text) #because int i = 0 is possible in a for, surprisingly!
            variables = findVariablesInThatMush(condition)
            if "int" in variables:
                variables.remove("int")
            print("tab = ", variables)
            listOfEveryPentads[i].addRole("loopCondition", None, variables)
        if(re.search(r'\{', listOfEveryPentads[i].text)):
            listOfEveryPentads[i].addRole("loopBeg", None, None)
        if(re.search(r'\}', listOfEveryPentads[i].text)):
            listOfEveryPentads[i].addRole("loopEnd", None, None)
    #printAllLoopCondVariables(targetFileListOfPentads)
    return spaceNormalizer(listOfEveryPentads)

def findVariablesInThatMush(string = None):
    print("MUSH printing --> ", "received : ", string)
    pattern = re.compile(r"""
        (?:[a-zA-Z_][\w]*) # a variable name
    """, re.VERBOSE)
    listOfVariables = list(set(re.findall(pattern, string))) #only unique elements
    return listOfVariables

def varDecDetector(listOfEveryPentads = None):
    """ Takes the entire pentad list, modifies all variable declarations and adds
        a role ("varDec", variable_name) to each line composing the declaration
        of a variable.

        Declarations of variables in C can extend over several lines. If this is
        the case, all the lines concerned will receive the role of the declaration.
        A declaration can also be made for several variables at the same time. This
        case is also taken into account, but another role will be created for each
        new variable declared on the same line.
        
        The initialization of variables, which can also take place at the time of
        their declaration, is not taken into account by this function, nor is the
        declaration of functions.
        
        Has not been implemented yet:
        * pointers
        _Bool
        __asm__ ou asm
        __attribute__ (par exemple : "  int x __attribute__ ((aligned (16))) = 0;  ") """

    presentChar = 'a'
    firstChar = 'a'
    secondChar = 'a'
    thirdChar = 'a'
    fourthChar = 'a'
    variableName = ""
    sequenceStartLine = 0
    state = "Waiting for int"
    for i in range (len(listOfEveryPentads)):
        listOfEveryPentads[i].text = varDecChangedToInt(listOfEveryPentads[i].text)
        #print(listOfEveryPentads[i].text)
        for j in range (len(listOfEveryPentads[i].text)):
            ######################################
            #line = listOfEveryPentads[i].text
            presentChar = listOfEveryPentads[i].text[j]
            #print("read : ", presentChar)
            if (j < len(listOfEveryPentads[i].text)-1) : firstChar = listOfEveryPentads[i].text[j+1]
            else: firstChar = None
            if (j < len(listOfEveryPentads[i].text)-2) : secondChar = listOfEveryPentads[i].text[j+2]
            else: secondChar = None
            if (j < len(listOfEveryPentads[i].text)-3) : thirdChar = listOfEveryPentads[i].text[j+3]
            else: thirdChar = None
            if (j < len(listOfEveryPentads[i].text)-4) : fourthChar = listOfEveryPentads[i].text[j+4]
            else: fourthChar = None
            ########## Thats a function ##########
            if(state == "Thats a function"):
                variableName = ""
                sequenceStartLine = 0                
                break
            ######################################
            if(state == "Waiting for variable name" and (presentChar == ' ' or presentChar == '\\')): # we need to keep it before "if(firstChar and secondChar...)"
                state = "Next valid char is variableName"                                             # because the real else condition is against " int\" and we
                #print(state)                                                                          # would need to repeat this twice as a elif (one against the " int\"
            elif(firstChar and secondChar and thirdChar and fourthChar):                              # and another time against the "if(firstChar and secondChar...)" !)
                if(presentChar == ' ' and firstChar == 'i' and secondChar == 'n' and  thirdChar == 't' and (fourthChar == ' ' or fourthChar == '\\')):
                    state = "Waiting for variable name"
                    #print(state)
                    sequenceStartLine = i
            if(state == "Next valid char is variableName" and presentChar != ' ' and presentChar != '\\'):
                state = "In variableName"
                #print(state)
            ######################################
            if(state == "In variableName" and presentChar != ' ' and presentChar != '\\' and presentChar != '=' and presentChar != ';' and presentChar != ','):
                variableName += listOfEveryPentads[i].text[j]
                #print("That's a variable :", variableName)
            if(state == "In variableName" and (presentChar == ' ' or presentChar == '\\' or presentChar == '=' or presentChar == ';' or presentChar == ',')):
                for k in range (sequenceStartLine, i+1):
                    listOfEveryPentads[k].addRole("varDeclar", variableName)
                    #print("I want to add role to line", k, " : varDec for ", variableName)
                variableName = ""
                state = "Is there another one ?"
            if(state == "Is there another one ?" and presentChar == ','):
                state = "Waiting for variable name"
                #print(state)
            if(state == "Is there another one ?" and presentChar == ';'):
                state = "Waiting for int"
                #print(state)
            ######################################
            if(state == "In variableName" and firstChar): # /!\ "int (a) = b" is a variable but "int a(b)" is a function /!\
                if(firstChar == '('):
                    state = "Thats a function"
                    #print(state)

    return listOfEveryPentads

def varDecChangedToInt(text = None):
    text = " " + text #to avoid variables named "integer123" or "myfloatvalue"
    text = text.replace(" unsigned long long ", " int ")
    text = text.replace(" unsigned long long\\", " int\\")
    text = text.replace(" unsigned long ", " int ")
    text = text.replace(" unsigned long\\", " int\\")
    text = text.replace(" unsigned int ", " int ")
    text = text.replace(" unsigned int\\", " int\\")
    text = text.replace(" unsigned short ", " int ")
    text = text.replace(" unsigned short\\", " int\\")
    text = text.replace(" unsigned char ", " int ")
    text = text.replace(" unsigned char\\", " int\\")
    text = text.replace(" signed char ", " int ")
    text = text.replace(" signed char\\", " int\\")
    text = text.replace(" long long int ", " int ")
    text = text.replace(" long long int\\", " int\\")
    text = text.replace(" short int ", " int ")
    text = text.replace(" short int\\", " int\\")
    text = text.replace(" long long ", " int ")
    text = text.replace(" long long\\", " int\\")
    text = text.replace(" long int ", " int ")
    text = text.replace(" long int\\", " int\\")
    text = text.replace(" long double ", " int ")
    text = text.replace(" long double\\", " int\\")
    text = text.replace(" long ", " int ")
    text = text.replace(" long\\", " int\\")
    text = text.replace(" char ", " int ")
    text = text.replace(" char\\", " int\\")
    text = text.replace(" short ", " int ")
    text = text.replace(" short\\", " int\\")
    text = text.replace(" float ", " int ")
    text = text.replace(" float\\", " int\\")
    text = text.replace(" double ", " int ")
    text = text.replace(" double\\", " int\\")
    return text


def varDefDetector(listOfEveryPentads = None):
    """ Takes the entire pentad list, select every variable that has been initialized
        one by one and adds for this variable a role ("varDef", variable_name) to each
        line where this variable value is changed.

        Value assignments in C can extend over several lines. If this is
        the case, all the lines concerned will receive the role of the declaration.
        An assignment can also be made for several variables at the same time. This
        case is also taken into account, but another role will be created for each
        new variable declared on the same line. """
    #https://regex101.com/r/rDvzLv/7

    i = 0
    for i in range (len(listOfEveryPentads)):
        listOfEveryPentads[i].text = ' ' + listOfEveryPentads[i].text #like always, it doesn't harm
        pattern = re.compile(r"""
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?<!=)                                                 # anything but an equal
            (?:=|\+=|\-=|\*=|\/=|%=|<<=|>>=|&=|\|=|\^=)            # an attribution operator
            (?!=)                                                  # anything but an equal
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<othervar>     # - - - - - - - - - - - - #
            (?:                                              #-----------------------
            -? (?:[\s]|[\\])*                           #    #     # symbol '-' or not then 0 or more spaces
            (?:                                              #  #--- EITHER ---
            (?:[a-zA-Z_][\w]*)                          #    #  #  # a variable name or
            | [\.\d]+                                        #  #  # one or more digits (floats included)
            | \"\"                                      #    #  #  # a string
            )                                                #  #--------------
            ){1}                                        #    #--------- 1x ---------
            (?:                                              #----------------------
            (?:[\s]|[\\])*                              #    #     # 0 or more spaces
            (?:\+|\-|\*|\/|%|<<|>>|\+\+|\-\-)+               #     # 1 or more arithmetic operators
            (?:[\s]|[\\])*                              #    #     # 0 or more spaces
            -? (?:[\s]|[\\])*                                #     # symbol '-' followed by 0 or more spaces
            (?:                                         #    #  #--- EITHER ---
            (?:[a-zA-Z_][\w]*)                               #  #  # a variable name or
            | [\.\d]+                                   #    #  #  # one or more digits (floats included)
            | \"\"                                           #  #  # a string
            )                                           #    #  #--------------
            )*                                               #------ 0 or more -----
            )                 # - - - - - - - - - - - - #
        """, re.VERBOSE)
        if(re.search(pattern, listOfEveryPentads[i].text)):
            found = re.findall(pattern, listOfEveryPentads[i].text)
            #print("FOR printing --> ", "first = ", found.group('first'), " second = ", found.group('second'))
            #print("FOR printing --> ", "before = ", listOfEveryPentads[i].text)
            #listOfEveryPentads[i].text = re.sub(pattern, found.group('first') + " " + found.group('second'), listOfEveryPentads[i].text)
            #print("FOR printing --> ", "after = ", listOfEveryPentads[i].text)
            for h in found :
                mainVar = h[0]
                otherVars = findVariablesInThatMush(h[1])
                print("tab = ", otherVars)
                listOfEveryPentads[i].addRole("varDefine", mainVar, otherVars)

    return listOfEveryPentads