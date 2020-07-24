from pentadClass import pentadStruct, printAllWithRoles, printAllVarDefVariables, printAllLoopCondVariables
from LexicalAnalyser import spaceNormalizer
import re

def mainSyntacticAnalyser(pentadList = [], debugMode = False):
    """This function calls every other functions in charge of the syntactic analyser and the syntactic
       transformations. It takes as arguments the list of PENTADS with the lines chopped into statements
       and returns the PENTADs list with roles updated. It also changes the text of the PENTADs in such a
       way that some useless informations are deleted."""
    if(debugMode) : print()
    if(debugMode) : print("——————————————————————————— SYNTACTIC ANALYSIS ——————————————————————————")
    if(debugMode) : print()
    if(debugMode) : print("MAIN printing --> ", "****** forLoopRoleAssignment *******")
    pentadList = forLoopRoleAssignment(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    #printAllLoopCondVariables(pentadList, debugMode)
    if(debugMode) : print("MAIN printing --> ", "********** varDecDetector **********")
    pentadList = varDecDetector(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    if(debugMode) : print("MAIN printing --> ", "********** varDefDetector **********")
    pentadList = varDefDetector(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    #printAllVarDefVariables(pentadList, debugMode)
    if(debugMode) : print()
    return pentadList

def forLoopRoleAssignment(listOfEveryPentads = None, debugMode = False):
    i = 0
    for i in range (len(listOfEveryPentads)):
        listOfEveryPentads[i].text = ' ' + listOfEveryPentads[i].text #for lines that start directly with "for"
        pattern = re.compile(r'(?P<first>\W|\0|^)for\s*(?P<second>(\(|\\|\0|$))')
        if(re.search(pattern, listOfEveryPentads[i].text)):
            found = re.search(pattern, listOfEveryPentads[i].text)
            if(debugMode) : print("FOR printing --> ", "first = ", found.group('first'), " second = ", found.group('second'))
            if(debugMode) : print("FOR printing --> ", "before = ", listOfEveryPentads[i].text)
            listOfEveryPentads[i].text = re.sub(pattern, found.group('first') + " " + found.group('second'), listOfEveryPentads[i].text)
            if(debugMode) : print("FOR printing --> ", "after = ", listOfEveryPentads[i].text)
            condition = varDecChangedToInt(listOfEveryPentads[i].text) #because int i = 0 is possible in a for, surprisingly!
            variables = findVariablesInThatMush(condition)
            if "int" in variables:
                variables.remove("int")
            if(debugMode) : print("tab = ", variables)
            listOfEveryPentads[i].addRole("loopCondition", None, variables)
        if(re.search(r'\{', listOfEveryPentads[i].text)):
            listOfEveryPentads[i].addRole("loopBeg", None, None)
        if(re.search(r'\}', listOfEveryPentads[i].text)):
            listOfEveryPentads[i].addRole("loopEnd", None, None)
    if(debugMode) : printAllLoopCondVariables(listOfEveryPentads)
    return spaceNormalizer(listOfEveryPentads, debugMode)

def findVariablesInThatMush(string = None, debugMode = False):
    if(debugMode) : print("MUSH printing --> ", "received : ", string)
    pattern = re.compile(r"""
        (?:[a-zA-Z_][\w]*) # a variable name
    """, re.VERBOSE)
    listOfVariables = list(set(re.findall(pattern, string))) #only unique elements
    return listOfVariables

def varDecDetector(listOfEveryPentads = None, debugMode = False):
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
        listOfEveryPentads[i].text = spacerForLoopConditions(listOfEveryPentads[i].text)
        listOfEveryPentads[i].text = varDecChangedToInt(listOfEveryPentads[i].text)
        if(debugMode) : print(listOfEveryPentads[i].text)
        for j in range (len(listOfEveryPentads[i].text)):
            ######################################
            #line = listOfEveryPentads[i].text
            presentChar = listOfEveryPentads[i].text[j]
            if(debugMode) : print("read : ", presentChar)
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
                if(debugMode) : print(state)                                                                          # would need to repeat this twice as a elif (one against the " int\"
            elif(firstChar and secondChar and thirdChar and fourthChar):                              # and another time against the "if(firstChar and secondChar...)" !)
                if(presentChar == ' ' and firstChar == 'i' and secondChar == 'n' and  thirdChar == 't' and (fourthChar == ' ' or fourthChar == '\\')):
                    state = "Waiting for variable name"
                    if(debugMode) : print(state)
                    sequenceStartLine = i
            if(state == "Next valid char is variableName" and presentChar != ' ' and presentChar != '\\'):
                state = "In variableName"
                if(debugMode) : print(state)
            ######################################
            if(state == "In variableName" and presentChar != ' ' and presentChar != '\\' and presentChar != '=' and presentChar != ';' and presentChar != ','):
                variableName += listOfEveryPentads[i].text[j]
                if(debugMode) : print("That's a variable :", variableName)
            if(state == "In variableName" and (presentChar == ' ' or presentChar == '\\' or presentChar == '=' or presentChar == ';' or presentChar == ',')):
                for k in range (sequenceStartLine, i+1):
                    listOfEveryPentads[k].addRole("varDeclar", variableName)
                    if(debugMode) : print("I want to add role to line", k, " : varDec for ", variableName)
                variableName = ""
                state = "Is there another one ?"
            if(state == "Is there another one ?" and presentChar == ','):
                state = "Waiting for variable name"
                if(debugMode) : print(state)
            if(state == "Is there another one ?" and presentChar == ';'):
                state = "Waiting for int"
                if(debugMode) : print(state)
            ######################################
            if(state == "In variableName" and firstChar): # /!\ "int (a) = b" is a variable but "int a(b)" is a function /!\
                if(firstChar == '('):
                    state = "Thats a function"
                    if(debugMode) : print(state)

    return spaceNormalizer(listOfEveryPentads, debugMode)

def spacerForLoopConditions(text = None, debugMode = False):
    text = " " + text
    text = text.replace("(", " ( ")
    text = text.replace(")", " ) ")
    text = text.replace(";", " ; ")
    return text

def varDecChangedToInt(text = None, debugMode = False):
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


def varDefDetector(listOfEveryPentads = None, debugMode = False):
    """ Takes the entire pentad list, select every variable that has been initialized
        one by one and adds for this variable a role ("varDef", variable_name) to each
        line where this variable value is changed.

        Value assignments in C can extend over several lines. If this is
        the case, all the lines concerned will receive the role of the declaration.
        An assignment can also be made for several variables at the same time. This
        case is also taken into account, but another role will be created for each
        new variable declared on the same line. """
    #https://regex101.com/r/rDvzLv/7

    #To solve the problem of var++ and var-- we are going to replace every one of these cases by "var += var"
    #To solve the problem of var1 += var2,  we are going to replace every one of these cases by "var1 = var1 +"


    i = 0
    for i in range (len(listOfEveryPentads)):
        listOfEveryPentads[i].text = ' ' + listOfEveryPentads[i].text #like always, it doesn't harm
###############################################################################################################
        pattern01 = re.compile(r"""
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?:\+\+)                                               # an increment operator
        """, re.VERBOSE)
        if(re.search(pattern01, listOfEveryPentads[i].text)):
            found = re.findall(pattern01, listOfEveryPentads[i].text)
            for h in found :
                mainVar = h[0]
                listOfEveryPentads[i].text = re.sub(pattern01, mainVar + " = " + mainVar + " + 1 ", listOfEveryPentads[i].text)
###############################################################################################################
        pattern02 = re.compile(r"""
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?:\-\-)                                               # a decrement operator
        """, re.VERBOSE)
        if(re.search(pattern02, listOfEveryPentads[i].text)):
            found = re.findall(pattern02, listOfEveryPentads[i].text)
            for h in found :
                mainVar = h[0]
                listOfEveryPentads[i].text = re.sub(pattern02, mainVar + " = " + mainVar + " - 1 ", listOfEveryPentads[i].text)
###############################################################################################################
        pattern03 = re.compile(r"""
            (?:\+\+)                                               # an increment operator
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
        """, re.VERBOSE)
        if(re.search(pattern03, listOfEveryPentads[i].text)):
            found = re.findall(pattern03, listOfEveryPentads[i].text)
            for h in found :
                mainVar = h[0]
                listOfEveryPentads[i].text = re.sub(pattern03, mainVar + " = " + mainVar + " + 1 ", listOfEveryPentads[i].text)
###############################################################################################################
        pattern04 = re.compile(r"""
            (?:\-\-)                                               # a decrement operator
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
        """, re.VERBOSE)
        if(re.search(pattern04, listOfEveryPentads[i].text)):
            found = re.findall(pattern04, listOfEveryPentads[i].text)
            for h in found :
                mainVar = h[0]
                listOfEveryPentads[i].text = re.sub(pattern04, mainVar + " = " + mainVar + " - 1 ", listOfEveryPentads[i].text)
###############################################################################################################
        pattern1 = re.compile(r"""
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<affectop>\+|\-|\*|\/|%|<<|>>|&|\||\^)              # an affectation operator
            (?:=)                                                  # an equal
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<othervar>     # - - - - - - - - - - - - #
            (?:                                              #-----------------------
            (?:-|~)? (?:[\s]|[\\])*                           #    #     # symbol '-' or '~' or not, then 0 or more spaces
            (?:                                              #  #--- EITHER ---
            (?:[a-zA-Z_][\w]*)                          #    #  #  # a variable name or
            | [\.\d]+                                        #  #  # one or more digits (floats included)
            | \"\"                                      #    #  #  # a string
            )                                                #  #--------------
            )?                                          #    #-------- 0 or 1 ------
            (?:                                              #----------------------
            (?:[\s]|[\\])*                              #    #     # 0 or more spaces
            (?:\+|\-|\*|\/|%|<<|>>|&|\||\^)+                 #     # 1 or more arithmetic operators
            (?:[\s]|[\\])*                              #    #     # 0 or more spaces
            (?:-|~)? (?:[\s]|[\\])*                                #     # symbol '-' or '~' or not, then 0 or more spaces
            (?:                                         #    #  #--- EITHER ---
            (?:[a-zA-Z_][\w]*)                               #  #  # a variable name or
            | [\.\d]+                                   #    #  #  # one or more digits (floats included)
            | \"\"                                           #  #  # a string
            )                                           #    #  #--------------
            )*                                               #------ 0 or more -----
            )                 # - - - - - - - - - - - - #
        """, re.VERBOSE)
        if(re.search(pattern1, listOfEveryPentads[i].text)):
            found = re.findall(pattern1, listOfEveryPentads[i].text)
            for h in found :
                mainVar = h[0]
                affectop = h[1]
                otherVars = h[2]
                listOfEveryPentads[i].text = re.sub(pattern1, mainVar + " = " + mainVar + affectop + " ( " + otherVars + " ) ", listOfEveryPentads[i].text)
###############################################################################################################
        pattern2 = re.compile(r"""
        (?P<mainvar>      # - - - - - - - - - - - - #
        (?:[a-zA-Z_][\w]*)                          #          # a variable name
        )                 # - - - - - - - - - - - - #
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?<!=)                                                 # anything but an equal
        (?:=)                                                  # an equal
        (?!=)                                                  # anything but an equal
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?P<othervar>     # - - - - - - - - - - - - #
        (?:                                              #-----------------------
        (?:[\s]|[\\])*                              #    #     # 0 or more spaces
        (?:[\(]|[\)])*                              #    #     # 0 or more parenthesis
        (?:[\s]|[\\])*                              #    #     # 0 or more spaces
        (?:-|~)? (?:[\s]|[\\])*                     #    #     # symbol '-' or '~' or not, then 0 or more spaces
        (?:                                              #  #--- EITHER ---
        (?:[a-zA-Z_][\w]*)                          #    #  #  # a variable name or
        | [\.\d]+                                        #  #  # one or more digits (floats included)
        | \"\"                                      #    #  #  # a string
        )                                                #  #--------------
        )?                                          #    #-------- 0 or 1 ------
        (?:                                              #----------------------
        (?:[\s]|[\\])*                              #    #     # 0 or more spaces
        (?:[\(]|[\)])*                              #    #     # 0 or more parenthesis
        (?:[\s]|[\\])*                              #    #     # 0 or more spaces
        (?:\+|\-|\*|\/|%|<<|>>|&|\||\^)+                 #     # 1 or more arithmetic operators
        (?:[\s]|[\\])*                              #    #     # 0 or more spaces
        (?:-|~)? (?:[\s]|[\\])*                          #     # symbol '-' or '~' or not, then 0 or more spaces
        (?:[\(]|[\)])*                              #    #     # 0 or more parenthesis
        (?:[\s]|[\\])*                              #    #     # 0 or more spaces
        (?:                                         #    #  #--- EITHER ---
        (?:[a-zA-Z_][\w]*)                               #  #  # a variable name or
        | [\.\d]+                                   #    #  #  # one or more digits (floats included)
        | \"\"                                           #  #  # a string
        )                                           #    #  #--------------
        (?:[\s]|[\\])*                              #    #     # 0 or more spaces
        (?:[\(]|[\)])*                              #    #     # 0 or more parenthesis
        )*                                               #------ 0 or more -----
        )                 # - - - - - - - - - - - - #
        """, re.VERBOSE)
        if(re.search(pattern2, listOfEveryPentads[i].text)):
            found = re.findall(pattern2, listOfEveryPentads[i].text)
            if(debugMode) : print("FOR printing --> ", "before = ", listOfEveryPentads[i].text)
            #listOfEveryPentads[i].text = re.sub(pattern2, found.group('first') + " " + found.group('second'), listOfEveryPentads[i].text)
            if(debugMode) : print("FOR printing --> ", "after = ", listOfEveryPentads[i].text)
            for h in found :
                mainVar = h[0]
                otherVars = findVariablesInThatMush(h[1])
                if(debugMode) : print("varDEF printing --> ", "tab = ", otherVars)
                listOfEveryPentads[i].addRole("varDefine", mainVar, otherVars)

    return spaceNormalizer(listOfEveryPentads, debugMode)