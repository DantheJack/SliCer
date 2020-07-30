from pentadClass import pentadStruct, printAllWithRoles, printAllVarDefVariables, printAllLoopCondVariables, printAllIfCondVariables
from LexicalAnalyser import spaceNormalizer, spacerForConditions
import re

def mainSyntacticAnalyser(pentadList = [], debugMode = False):
    """This function calls every other functions in charge of the syntactic analyser and the syntactic
       transformations. It takes as arguments the list of PENTADS with the lines chopped into statements
       and returns the PENTADs list with roles updated."""
    if(debugMode) : print()
    if(debugMode) : print("——————————————————————————— SYNTACTIC ANALYSIS ——————————————————————————")
    if(debugMode) : print()
    if(debugMode) : print("MAIN printing --> ", "****** loopRoleAssignment *******")
    pentadList = loopRoleAssignment(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    #printAllLoopCondVariables(pentadList, debugMode)
    if(debugMode) : print("MAIN printing --> ", "****** ifRoleAssignment *******")
    pentadList = ifRoleAssignment(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    if(debugMode) : print("MAIN printing --> ", "****** elseRoleAssignment *******")
    pentadList = elseRoleAssignment(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    if(debugMode) : print("MAIN printing --> ", "********** varDefDetector **********")
    pentadList = varDefDetector(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    #printAllVarDefVariables(pentadList, debugMode)
    if(debugMode) : print("MAIN printing --> ", "********** varScanDetector **********")
    pentadList = scanVarDetector(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    if(debugMode) : print("MAIN printing --> ", "********** varDecDetector **********")
    pentadList = varDecDetector(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)
    if(debugMode) : print()
    return pentadList

def loopRoleAssignment(pentadList = None, debugMode = False, executedManyTimes = 0):
    executedManyTimes = executedManyTimes + 1
    if(executedManyTimes == 150) : return []
    recursiveCase = False
    i = 0
    bracketsCounter = 0
    listOfRoles = []
    loopStarted = False
    loopConditionStatementId = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #for lines that start directly with "for"
        patternCond = re.compile(r'(?P<first>\W|\0|^)for\s*(?P<second>(\(|\\|\0|$))')
        if(re.search(patternCond, pentadList[i].text)):
            if(loopStarted):
                recursiveCase = True
            else :
                listOfRoles = []
                for role in pentadList[i].roles :
                    listOfRoles += [role.type]
                if(debugMode) : print("FORrole printing --> ", "line", i, "already has roles :", listOfRoles)
                if(not "loopCondition" in listOfRoles):
                    variables = findVariablesInThatMush(pentadList[i].text, debugMode)
                    if "for" in variables:
                        variables.remove("for")
                    if "int" in variables:
                        variables.remove("int")
                    pentadList[i].addRole("loopCondition", None, variables)
                    listOfRoles += ["loopCondition"]
                    loopStarted = True
                    loopConditionStatementId = i
        elif(loopStarted):
            if("loopCondition" in listOfRoles):
                pentadList[i].addRole("loopBeg", str(loopConditionStatementId), None)
                bracketsCounter = 1        
                listOfRoles = []
            elif(re.search(r'\{', pentadList[i].text)):
                bracketsCounter += 1 
            if(re.search(r'\}', pentadList[i].text)):
                bracketsCounter -= 1 
                if(bracketsCounter == 0):
                    loopStarted = False
                    listOfRoles = []
                    pentadList[i].addRole("loopEnd", str(loopConditionStatementId), None)
    if(recursiveCase):
        return loopRoleAssignment(spaceNormalizer(pentadList, False), debugMode, executedManyTimes)
    if(debugMode) : printAllWithRoles(pentadList)
    return spaceNormalizer(pentadList, debugMode)




def findVariablesInThatMush(string = None, debugMode = False):
    if(debugMode) : print("MUSH printing --> ", "received : ", string)
    pattern = re.compile(r"""
        (?:[a-zA-Z_][\w]*) # a variable name
    """, re.VERBOSE)
    listOfVariables = list(set(re.findall(pattern, string))) #only unique elements
    return listOfVariables

def varDecDetector(pentadList = None, debugMode = False):
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
    for i in range (len(pentadList)):
        pentadList[i].text = spacerForConditions(pentadList[i].text)
        pentadList[i].text = varDecChangedToInt(pentadList[i].text)
        if(debugMode) : print(pentadList[i].text)
        for j in range (len(pentadList[i].text)):
            ######################################
            #line = pentadList[i].text
            presentChar = pentadList[i].text[j]
            if(debugMode) : print("varDEC printing --> ", "read : ", presentChar)
            if (j < len(pentadList[i].text)-1) : firstChar = pentadList[i].text[j+1]
            else: firstChar = None
            if (j < len(pentadList[i].text)-2) : secondChar = pentadList[i].text[j+2]
            else: secondChar = None
            if (j < len(pentadList[i].text)-3) : thirdChar = pentadList[i].text[j+3]
            else: thirdChar = None
            if (j < len(pentadList[i].text)-4) : fourthChar = pentadList[i].text[j+4]
            else: fourthChar = None
            ########## Thats a function ##########
            if(state == "Thats a function"):
                variableName = ""
                sequenceStartLine = 0                
                break
            ########## Thats a tab ##########
            if(state == "Thats a tab" and presentChar == ']'):
                if(variableName != "") :
                    for k in range (sequenceStartLine, i+1):
                        pentadList[k].addRole("varDeclar", variableName)
                        if(debugMode) : print("varDEC printing --> ", "I want to add role to line", k, " : varDec for ", variableName)
                variableName = ""
                if(firstChar == ' ' or firstChar == '\\' or firstChar == '=' or firstChar == ';' or firstChar == ','):
                    state = "Is there another one ?"
            ######################################
            if(state == "Waiting for variable name" and (presentChar == ' ' or presentChar == '\\')): # we need to keep it before "if(firstChar and secondChar...)"
                state = "Next valid char is variableName"                                             # because the real else condition is against " int\" and we
                if(debugMode) : print("varDEC printing --> ", state)                                                                          # would need to repeat this twice as a elif (one against the " int\"
            elif(firstChar and secondChar and thirdChar and fourthChar):                              # and another time against the "if(firstChar and secondChar...)" !)
                if(presentChar == ' ' and firstChar == 'i' and secondChar == 'n' and  thirdChar == 't' and (fourthChar == ' ' or fourthChar == '\\')):
                    state = "Waiting for variable name"
                    if(debugMode) : print("varDEC printing --> ", state)
                    sequenceStartLine = i
            if(state == "Next valid char is variableName" and presentChar != ' ' and presentChar != '\\'):
                state = "In variableName"
                if(debugMode) : print("varDEC printing --> ", "varDEC printing --> ", state)
            ######################################
            if(state == "In variableName" and presentChar != ' ' and presentChar != '\\' and presentChar != '=' and presentChar != ';' and presentChar != ','):
                variableName += pentadList[i].text[j]
                if(debugMode) : print("varDEC printing --> ", "That's a variable :", variableName)
            if(state == "In variableName" and (presentChar == ' ' or presentChar == '\\' or presentChar == '=' or presentChar == ';' or presentChar == ',')):
                for k in range (sequenceStartLine, i+1):
                    pentadList[k].addRole("varDeclar", variableName)
                    if(debugMode) : print("varDEC printing --> ", "I want to add role to line", k, " : varDec for ", variableName)
                variableName = ""
                state = "Is there another one ?"
            if(state == "Is there another one ?" and presentChar == ','):
                state = "Waiting for variable name"
                if(debugMode) : print("varDEC printing --> ", state)
            if(state == "Is there another one ?" and presentChar == ';'):
                state = "Waiting for int"
                if(debugMode) : print("varDEC printing --> ", state)
            ######################################
            if(state == "In variableName" and firstChar): # /!\ "int (a) = b" is a variable but "int a(b)" is a function /!\
                if(firstChar == '('):
                    state = "Thats a function"
                    if(debugMode) : print("varDEC printing --> ", state)
            ######################################
            if(state == "In variableName" and firstChar): # /!\ "int (a) = b" is a variable but "int a(b)" is a function /!\
                if(firstChar == '['):
                    state = "Thats a tab"
                    if(debugMode) : print("varDEC printing --> ", state)

    return spaceNormalizer(pentadList, debugMode)

def varDecChangedToInt(text = None, debugMode = False):
    text = " " + text #to avoid variables named "integer123" or "myfloatvalue"
    text = text.replace(",", " , ")
    text = text.replace(" FILE *", " int ")
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


def varDefDetector(pentadList = None, debugMode = False):
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
    #To solve the problem of var1 += ... ,  we are going to replace every one of these cases by "var1 = var1 + (...)"


    i = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #like always, it doesn't harm
###############################################################################################################
        pattern01 = re.compile(r"""
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?:\+\+)                                               # an increment operator
        """, re.VERBOSE)
        if(re.search(pattern01, pentadList[i].text)):
            found = re.findall(pattern01, pentadList[i].text)
            for h in found :
                mainVar = h[0]
                pentadList[i].text = re.sub(pattern01, mainVar + " = " + mainVar + " + 1 ", pentadList[i].text)
###############################################################################################################
        pattern02 = re.compile(r"""
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?:\-\-)                                               # a decrement operator
        """, re.VERBOSE)
        if(re.search(pattern02, pentadList[i].text)):
            found = re.findall(pattern02, pentadList[i].text)
            for h in found :
                mainVar = h[0]
                pentadList[i].text = re.sub(pattern02, mainVar + " = " + mainVar + " - 1 ", pentadList[i].text)
###############################################################################################################
        pattern03 = re.compile(r"""
            (?:\+\+)                                               # an increment operator
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
        """, re.VERBOSE)
        if(re.search(pattern03, pentadList[i].text)):
            found = re.findall(pattern03, pentadList[i].text)
            for h in found :
                mainVar = h[0]
                pentadList[i].text = re.sub(pattern03, mainVar + " = " + mainVar + " + 1 ", pentadList[i].text)
###############################################################################################################
        pattern04 = re.compile(r"""
            (?:\-\-)                                               # a decrement operator
            (?:[\s]|[\\])*                                         # 0 or more spaces
            (?P<mainvar>      # - - - - - - - - - - - - #
            (?:[a-zA-Z_][\w]*)                          #          # a variable name
            )                 # - - - - - - - - - - - - #
            (?:[\s]|[\\])*                                         # 0 or more spaces
        """, re.VERBOSE)
        if(re.search(pattern04, pentadList[i].text)):
            found = re.findall(pattern04, pentadList[i].text)
            for h in found :
                mainVar = h[0]
                pentadList[i].text = re.sub(pattern04, mainVar + " = " + mainVar + " - 1 ", pentadList[i].text)
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
        if(re.search(pattern1, pentadList[i].text)):
            found = re.findall(pattern1, pentadList[i].text)
            for h in found :
                mainVar = h[0]
                affectop = h[1]
                otherVars = h[2]
                pentadList[i].text = re.sub(pattern1, mainVar + " = " + mainVar + affectop + " ( " + otherVars + " ) ", pentadList[i].text)
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
        if(re.search(pattern2, pentadList[i].text)):
            found = re.findall(pattern2, pentadList[i].text)
            for h in found :
                mainVar = h[0]
                otherVars = findVariablesInThatMush(h[1], debugMode)
                if(debugMode) : print("varDEF printing --> ", "tab = ", otherVars)
                pentadList[i].addRole("varDefine", mainVar, otherVars)

    return spaceNormalizer(pentadList, debugMode)


def scanVarDetector(pentadList = [], debugMode = False):
    """ Takes the entire pentad list, select every scanf or gets (any user entry for
        variable definition) and adds for this variable a role ("varDef", variable_name) 
        to each line where this variable value is changed.

        scanf-like functions, in C language, can extend over several lines. If this is
        the case, all the lines concerned will receive the role of the declaration.
        An scan can also be made for several variables at the same time. This
        case is also taken into account, but another role will be created for each
        new variable declared on the same line. """
    i = 0
    for i in range (len(pentadList)):
        pentadList[i].text = pentadList[i].text.replace("getchar()", " 0 ")                
        pentadList[i].text = pentadList[i].text.replace("getchar ()", " 0 ")               
        pentadList[i].text = pentadList[i].text.replace("getchar( )", " 0 ")               
        pentadList[i].text = pentadList[i].text.replace("getchar ( )", " 0 ") #no need to do more than 1 space thanks to spaceNormailizer
                                                                                           # int getchar(void);
###############################################################################################################
    i = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #like always, it doesn't harm
        pattern1 = re.compile(r"""
        (?:[\s]|[\\]|\0|^)+                                    # start of a keyword
        (?:fgets|gets)                                         # an entry keyword
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:\()                                                 # a parenthesis
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?P<variable>  
        (?:[a-zA-Z_][\w]*)                                     # a variable name
        )
        """, re.VERBOSE)
        if(re.search(pattern1, pentadList[i].text)):
            found = re.findall(pattern1, pentadList[i].text)
            for h in found :
                variables = findVariablesInThatMush(h, debugMode)
                for var in variables:
                    if(debugMode) : print("varSCAN printing --> ", "scanned = ", var)
                    pentadList[i].addRole("varDefine", var)
                                                                 #char *fgets(char *s, int size, FILE *stream);
###############################################################################################################
        pattern2 = re.compile(r"""
        (?:scanf|fscanf|sscanf)                                # a scanf-like keyword
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:\()                                                 # a parenthesis
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:\".*?\")                                            # anything between quotes
        (?P<variables>  
        (?:                                              #-----------------------
        (?:[\s]|[\\])*                                   #     # 0 or more spaces
        (?:,)(?:[\s]|[\\])*                              #     # a ',' then 0 or more spaces
        (?:&)?                                           #     # symbol '&' or not
        (?:[\s]|[\\])*                                   #     # 0 or more spaces
        (?:[\(]|[\)])*                                   #     # 0 or more parenthesis
        (?:[\s]|[\\])*                                   #     # 0 or more spaces
        (?:[a-zA-Z_][\w]*)                               #     # a variable name
        )+                                               #-------- 1 or more ------
        )                
        """, re.VERBOSE)
        if(re.search(pattern2, pentadList[i].text)):
            found = re.findall(pattern2, pentadList[i].text)
            for h in found :
                variables = findVariablesInThatMush(h, debugMode)
                for var in variables:
                    if(debugMode) : print("varSCAN printing --> ", "scanned = ", var)
                    pentadList[i].addRole("varDefine", var)
                                                                                                       # scanf;
############################################################################################################### 
    i = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #like always, it doesn't harm
        pattern3 = re.compile(r"""
        (?:ungetc)                                             # an entry keyword
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:\()                                                 # a parenthesis
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:&)?                                                 # symbol '&' or not
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:[\(]|[\)])*                                         # 0 or more parenthesis
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?P<variable>
        (?:[a-zA-Z_][\w]*)                                     # a variable name or
        | [\.\d]+                                              # one or more digits (floats included)
        | \"\" | \'.\'                                         # a string or a char
        )
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:,)(?:[\s]|[\\])*                                    # a ',' then 0 or more spaces
        (?:.)*?                                                # anything
        (?:\))                                                 # a parenthesis
        """, re.VERBOSE)
        if(re.search(pattern3, pentadList[i].text)):
            found = re.findall(pattern3, pentadList[i].text)
            pentadList[i].text = re.sub(pattern3, found[0][0], pentadList[i].text)
                                                                                     #int ungetc(FILE *stream);
############################################################################################################### 
    i = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #like always, it doesn't harm
        pattern4 = re.compile(r"""
        (?:[\s]|[\\]|\0|^)+                                    # start of a keyword
        (?:getc|fgetc)                                         # an entry keyword
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:\()                                                 # a parenthesis
        (?:.)*?                                                # anything
        (?:\))                                                 # a parenthesis
        """, re.VERBOSE)
        if(re.search(pattern4, pentadList[i].text)):
            found = re.findall(pattern4, pentadList[i].text)
            pentadList[i].text = re.sub(pattern4, " 0 ", pentadList[i].text)
                                                                                      # int getc(FILE *stream);
                                                                                     # int fgetc(FILE *stream);
###############################################################################################################
    return spaceNormalizer(pentadList, debugMode)

def ifRoleAssignment(pentadList = None, debugMode = False, executedManyTimes = 0):
    executedManyTimes = executedManyTimes + 1
    if(executedManyTimes == 150) : return []
    recursiveCase = False
    i = 0
    bracketsCounter = 0
    listOfRoles = []
    ifStarted = False
    ifConditionStatementId = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #for lines that start directly with "for"
        patternCond = re.compile(r'(?P<first>\W|\0|^)if\s*(?P<second>(\(|\\|\0|$))')
        if(re.search(patternCond, pentadList[i].text)):
            if(ifStarted):
                recursiveCase = True
            else :
                listOfRoles = []
                for role in pentadList[i].roles :
                    listOfRoles += [role.type]
                if(debugMode) : print("IFrole printing --> ", "line", i, "already has roles :", listOfRoles)
                if(not "ifCondition" in listOfRoles):
                    variables = findVariablesInThatMush(pentadList[i].text, debugMode)
                    if "if" in variables:
                        variables.remove("if")
                    pentadList[i].addRole("ifCondition", None, variables)
                    listOfRoles += ["ifCondition"]
                    ifStarted = True
                    ifConditionStatementId = i
        elif(ifStarted):
            if("ifCondition" in listOfRoles):
                pentadList[i].addRole("ifBeg", str(ifConditionStatementId), None)
                bracketsCounter = 1        
                listOfRoles = []
            elif(re.search(r'\{', pentadList[i].text)):
                bracketsCounter += 1 
            if(re.search(r'\}', pentadList[i].text)):
                bracketsCounter -= 1 
                if(bracketsCounter == 0):
                    ifStarted = False
                    listOfRoles = []
                    pentadList[i].addRole("ifEnd", str(ifConditionStatementId), None)
    if(recursiveCase):
        return ifRoleAssignment(spaceNormalizer(pentadList, False), debugMode, executedManyTimes)
    if(debugMode) : printAllWithRoles(pentadList)
    return spaceNormalizer(pentadList, debugMode)

def elseRoleAssignment(pentadList = None, debugMode = False, executedManyTimes = 0):
    executedManyTimes = executedManyTimes + 1
    if(executedManyTimes == 150) : return []
    recursiveCase = False
    i = 0
    bracketsCounter = 0
    listOfRoles = []
    elseStarted = False
    elseConditionStatementId = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #for lines that start directly with "for"
        patternCond = re.compile(r'(\W|\0|^)else\s*(\\|\0|$)')
        if(re.search(patternCond, pentadList[i].text)):
            if(elseStarted):
                recursiveCase = True
            else :
                listOfRoles = []
                for role in pentadList[i].roles :
                    listOfRoles += [role.type]
                if(debugMode) : print("IFrole printing --> ", "line", i, "already has roles :", listOfRoles)
                if(not "elseCondition" in listOfRoles):
                    pentadList[i].addRole("elseCondition", None, None)
                    listOfRoles += ["elseCondition"]
                    elseStarted = True
                    elseConditionStatementId = i
        elif(elseStarted):
            if("elseCondition" in listOfRoles):
                pentadList[i].addRole("elseBeg", str(elseConditionStatementId), None)
                bracketsCounter = 1        
                listOfRoles = []
            elif(re.search(r'\{', pentadList[i].text)):
                bracketsCounter += 1 
            if(re.search(r'\}', pentadList[i].text)):
                bracketsCounter -= 1 
                if(bracketsCounter == 0):
                    elseStarted = False
                    listOfRoles = []
                    pentadList[i].addRole("elseEnd", str(elseConditionStatementId), None)
    if(recursiveCase):
        return elseRoleAssignment(spaceNormalizer(pentadList, False), debugMode, executedManyTimes)
    if(debugMode) : printAllWithRoles(pentadList)
    return spaceNormalizer(pentadList, debugMode)