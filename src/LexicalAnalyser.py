from pentadClass import pentadStruct, printAll, printAllWithRoles
import re
import sys

def mainLexicalAnalyser(fileCompletePath = "", debugMode = False):
    """This function calls every other functions in charge of the lexical analyser and the transformations
       that aim at making the original code easier to read/understand/chop from a computer point of view. 
       It takes as arguments the file path (including the name and the extension) and returns the PENTADs
       list where each line has been divided into statements and the list of every text line from the orginal
       code. It also changes the text of the PENTADs in such a
       way that some useless informations are deleted, like the removal of every string and every comment."""
    if(debugMode) : print()
    if(debugMode) : print("———————————————————————————— LEXICAL ANALYSIS ———————————————————————————")
    if(debugMode) : print()
    if(debugMode) : print("MAIN printing --> ", "*********** readlines ************")
    targetFile = open(fileCompletePath, "r")
    targetFileAllTextLines = targetFile.readlines()                 
    targetFile.close()
    pentadList = []
    pentadList.append(pentadStruct([0], "")) # just to start at pentadList[1]
    for textLine in range (len(targetFileAllTextLines)):
        newPentad = pentadStruct([textLine], targetFileAllTextLines[textLine])
        pentadList.append(newPentad)
    pentadList.append(pentadStruct([0], "//")) # because stringReducer (and maybe others) have troubles dealing with the very last PENTAD of the list
    if(debugMode) : print("MAIN printing --> ", "********* spaceNormalizer ********") 
    pentadList = spaceNormalizer(spaceNormalizer(pentadList))
    if(debugMode) : printAll(pentadList)
    if(debugMode) : print("MAIN printing --> ", "********* commentsEraser *********")
    pentadList = commentsEraser(pentadList, False)
    if(debugMode) : printAll(pentadList)
    empty = True
    for i in pentadList:
        if(len(i.text) > 1):
            empty = False
    if (empty) :
        if(debugMode) :
            sys.exit(1)
        return [[], targetFileAllTextLines]
    if(debugMode) : print("MAIN printing --> ", "********* stringReducer **********")
    pentadList = stringReducer(pentadList, True)
    if(debugMode) : printAll(pentadList)
    if(debugMode) : print("MAIN printing --> ", "******** doWhileConverter ********")
    pentadList = doWhileConverter(pentadList, False)
    if(debugMode) : printAllWithRoles(pentadList)
    if(len(pentadList) < 1):
        if(debugMode) : sys.exit(1)
        return [[], targetFileAllTextLines]
    if(debugMode) : print("MAIN printing --> ", "******** whileLoopConverter ********")
    pentadList = whileLoopConverter(pentadList, False)
    if(debugMode) : printAllWithRoles(pentadList)
    if(len(pentadList) < 1):
        if(debugMode) : sys.exit(1)
        return [[], targetFileAllTextLines]
    if(debugMode) : print("MAIN printing --> ", "******* semicolonBasedChopper *******")
    pentadList = semicolonBasedChopper(pentadList, debugMode)
    if(len(pentadList) < 1):
        if(debugMode) : sys.exit(1)
        return [[], targetFileAllTextLines]
    if(debugMode) : printAllWithRoles(pentadList)
    #to see line count : for i in range (len(pentadList)):
    #to see line count :     print("st = ", i, " | lines = [", pentadList[i].lines[0], "," , pentadList[i].lines[1], "] | len = ", len(pentadList[i].text), " | read : " , pentadList[i].text)
    if(debugMode) : print("MAIN printing --> ", "******* ifNormalizer *******")
    pentadList = ifNormalizer(pentadList, debugMode)
    if(len(pentadList) < 1):
        if(debugMode) : sys.exit(1)
        return [[], targetFileAllTextLines]
    if(debugMode) : printAllWithRoles(pentadList)
    #to see line count : for i in range (len(pentadList)):
    #to see line count :     print("st = ", i, " | lines = [", pentadList[i].lines[0], "," , pentadList[i].lines[1], "] | len = ", len(pentadList[i].text), " | read : " , pentadList[i].text)
    if(debugMode) : print("MAIN printing --> ", "******* elseNormalizer *******")
    pentadList = elseNormalizer(pentadList, debugMode)
    if(len(pentadList) < 1):
        if(debugMode) : sys.exit(1)
        return [[], targetFileAllTextLines]
    if(debugMode) : printAllWithRoles(pentadList)

    if(debugMode) : print("MAIN printing --> ", "********** multiLineManager *********")
    if(len(pentadList) < 1):
        if(debugMode) : sys.exit(1)
        return [[], targetFileAllTextLines]
    pentadList = multiLineManager(pentadList, debugMode)
    if(debugMode) : printAllWithRoles(pentadList)

    return [pentadList, targetFileAllTextLines]

def spacerForConditions(text = None, debugMode = False):
    text = " " + text
    text = text.replace("(", " ( ")
    text = text.replace(")", " ) ")
    text = text.replace(";", " ; ")
    #text = text.replace("=", " = ") #bad idea because of ==
    return text

def spaceNormalizer(pentadList = [], debugMode = False):
    """Takes the list of all pentads and returns this list with the
    modified text elements so that unnecessary spaces are removed.
    
    The strings we manipulate come from the C language, but this
    language is not space sensitive, meaning that it is possible
    to add spaces anywhere in the code where it is already
    syntactically correct to find a single space. To simplify
    the analysis of the code, we will remove all multiple spaces
    by reducing them to a single space. """
    outputbefore = []
    outputafter = []
    #line = ""
    presentChar = 'a'
    nextChar = 'a'
    stringStatement = "Nothing"
    for i in range (len(pentadList)):
        outputbefore.append(pentadStruct(pentadList[i].lines, ""))
        if (stringStatement == "Nothing") :
            spacerForConditions(pentadList[i].text, debugMode)
            pentadList[i].text = pentadList[i].text.lstrip() #remove every space before the first character
            if(debugMode) : print("lstrip outputbefore[" + str(i) + "].text = |" + outputbefore[i].text + "|")
        for j in range (len(pentadList[i].text)):
            ######################################
            #line = outputbefore[i].text
            presentChar = pentadList[i].text[j]
            if (j < len(pentadList[i].text)-1) :
                nextChar = pentadList[i].text[j+1]
            else:
                nextChar = None
            ######################################
            if (stringStatement == "Nothing" and presentChar == "\"") :
                stringStatement = "Going"
            elif (stringStatement == "Going" and presentChar == "\"") :
                stringStatement = "Nothing"
            if (stringStatement == "Going" and presentChar != '\n') :
                outputbefore[i].text += pentadList[i].text[j]
                if(debugMode) : print("outputbefore[" + str(i) + "].text = |" + outputbefore[i].text + "|")
            elif (not (presentChar==" " and (nextChar == " " or nextChar == None or nextChar == "\n")) and presentChar != '\n'):
                outputbefore[i].text += pentadList[i].text[j]
                if(debugMode) : print("outputbefore[" + str(i) + "].text = |" + outputbefore[i].text + "|")
        if (stringStatement == "Nothing") :
            outputbefore[i].text.rstrip() #remove every space after the last character
            if(debugMode) : print("rstrip outputbefore[" + str(i) + "].text = |" + outputbefore[i].text + "|")
            for role in pentadList[i].roles:
                outputbefore[i].addRole(role.type, role.mainVar, role.otherVars)
    for i in range (len(pentadList)):
        if(len(pentadList[i].text) > 0):
            outputafter.append(outputbefore[i])   
    return outputafter

def commentsEraser(pentadList = [], debugMode = False):
    """ Takes the complete list of pentads and returns this list once all
        comments have been removed.

        Of course, the line count does not change. Comments, whether they
        are multiline (/* */) or monoline (//), are removed in such a way
        that it disrupts the structure of the executable code as little as
        possible. This is the whole difference between a home-made function
        and the work of the preprocessor. The current code also takes into
        account the case of comment symbols that actually belong to strings.
        Example: printf("/** _this should be printed_ **/ // _that too_"). 
        
        However, in C, if a monoline comment ends with \\, the next line is
        considered as part of the actual line and is supposed to be part of
        the comment as well. This case has not been implemented yet. """
    output = []
    multiLineComment = "Nothing"
    stringStatement = "Nothing"
    presentChar = 'a'
    nextChar = 'a'
    singleLineCommentDetected = False
    i = 0
    for i in range (len(pentadList)):
        ########### Variables #############
        singleLineCommentDetected = False
        output.append(pentadStruct([i,i], ""))
        for j in range (len(pentadList[i].text)):
            presentChar = pentadList[i].text[j]
            if (j < len(pentadList[i].text)-1) :
                nextChar = pentadList[i].text[j+1]
            else:
                nextChar = None
        ##########################################
            ########### String Management #############
            if(not singleLineCommentDetected and (multiLineComment == "Nothing" or multiLineComment == "Ended")) : # We can be in a String but not having changed "Ended" to "Nothing" yet
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  # 
                if stringStatement == "Started" : stringStatement = "Going"
                if stringStatement == "Ended" : stringStatement = "Nothing"
                if(presentChar == "\"") :
                    if(stringStatement == "Going") :
                        if(j == 0 ):
                            stringStatement = "Ended"
                            if(debugMode) : print("String ended line : " + str(i)) 
                        elif(pentadList[i].text[j-1] != '\\'):
                            stringStatement = "Ended"
                            if(debugMode) : print("String ended line : " + str(i)) 
                    elif(stringStatement == "Nothing") :
                        stringStatement = "Started"
                        if(debugMode) : print("String started line : " + str(i))
            ##########################################
            ########### Multi Management #############
            if(not singleLineCommentDetected and (stringStatement == "Nothing" or stringStatement == "Started")): # We can be IN THE STATE "Ended" but also in a String already
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  # 
                if multiLineComment == "Almost started" : multiLineComment = "Started"
                elif multiLineComment == "Started" : multiLineComment = "Going"
                if multiLineComment == "Almost done" : multiLineComment = "Ended"
                elif multiLineComment == "Ended" : multiLineComment = "Nothing" 
                if multiLineComment == "Going" : #from "Going" we can immediatly be in "Almost done" if we have : /**/
                    if(presentChar == "*" and nextChar != None) :
                        if nextChar == "/" : multiLineComment = "Almost done"
                ###################################
                if(presentChar == "/" and nextChar and multiLineComment == "Nothing"):
                    if nextChar == "/" : singleLineCommentDetected = True
                    elif nextChar == "*" and not singleLineCommentDetected : multiLineComment = "Almost started"
            ########### Last Line ############
            if(not singleLineCommentDetected and multiLineComment == "Nothing"):
                output[i].text += pentadList[i].text[j]
    return spaceNormalizer(output, debugMode)

def stringReducer(pentadList = [], debugMode = False):
    """ Takes the entire original code and replace every "string" by
    an empty string like that: "". This, because the content of the strings does not
    matter for slicing, and because we can make sure that nowhere in the code
    we will find a key word such as "loop", "while" or "unsigned int" apart from
    where they are actually meaningful (we already took care of the comments at
    this point)."""
    output = []
    currentStatement = ""
    presentChar = 'a'
    nextChar = 'a'
    inAString = False
    escapingChar = "No"
    i = 0
    for i in range (len(pentadList)):
        for j in range (len(pentadList[i].text)):
            ########### Variables #############
            presentChar = pentadList[i].text[j]
            if (j < len(pentadList[i].text)-1) :
                nextChar = pentadList[i].text[j+1]
            else:
                nextChar = None
            ##########################################
            if(debugMode) : print("line = ", i, " | j =", j, " | len = ", len(pentadList[i].text), " | read : " , presentChar)
            if(escapingChar == "Next one"):
                escapingChar = "This char"
            elif(escapingChar == "This char"):
                escapingChar = "No"
            if(presentChar == "\"" and escapingChar != "This char"):
                inAString = not inAString
                currentStatement += "\""
                if(debugMode) : print("STRRED printing --> ", "char \' \" \' added to", currentStatement)
            elif(inAString):
                if(debugMode) : print("STRRED printing --> ", "We're in a string, no char added")
                if(presentChar == '\\' and nextChar != '\n'):
                    escapingChar = "Next one"
            else:
                currentStatement += presentChar
                if(debugMode) : print("STRRED printing --> ", "char \'", presentChar, "\' added to", currentStatement)

        output.append(pentadStruct([pentadList[i].lines[0], pentadList[i].lines[1]], currentStatement))
        currentStatement = ""    
    #output.append(pentadStruct([startingLine, i], currentStatement))   
    return spaceNormalizer(output, debugMode)

def semicolonBasedChopper(pentadList = [], debugMode = False):
    """This function separates statement using ';' as a limitation point."""
    pentadList = spaceNormalizer(pentadList, False)
    ### Always, no... ALWAYS ! ALWAYS KEEP RUN SPACENORMALIZER BEFORE CHOP-CHOP.   ALWAYS !!!!!!!!!
    ## (because spaces in beginning and end of lines can cause ifs and elses to overspread)
    # ...
    # ALWAYS !!!
    #
    output = []
    currentStatement = ""
    presentChar = 'a'
    startingLine = 0
    inLoopCondition = False
    i = 0
    nextChar = None
    lineOfTheLastCharRead = 0
    for i in range (len(pentadList)):
        if(debugMode) : print("st = ", i, " | lines = [", pentadList[i].lines[0], "," , pentadList[i].lines[1], "] | len = ", len(pentadList[i].text), " | read : " , pentadList[i].text)
        pattern = re.compile(r'(?P<all>(\W|\0|^)for)(?=\()')
        found = re.search(pattern, pentadList[i].text)
        safetyBreakPoint = 0
        while(found != None):
            if(debugMode) : print ("found : " + found.group('all'))
            if(debugMode) : print("line before : ", pentadList[i].text)
            pentadList[i].text = re.sub(pattern, found.group('all')+" ", pentadList[i].text, 1)
            if(debugMode) : print("line after  : ", pentadList[i].text)
            pattern = re.compile(r'(?P<all>(\W|\0|^)for)(?=\()')
            found = re.search(pattern, pentadList[i].text)
            safetyBreakPoint = safetyBreakPoint + 1
            if safetyBreakPoint == 1000 : break

    for i in range (len(pentadList)):
        ########### Variables #############
        for j in range (len(pentadList[i].text)):
            notAddedYet = True
            presentChar = pentadList[i].text[j]
            if (j < len(pentadList[i].text)-1) :
                nextChar = pentadList[i].text[j+1]
            else:
                nextChar = None
            if(currentStatement == ""):
                if(debugMode) : print("semiBC printing --> ", "No char yet in the buffer. --> startingLine = ", pentadList[i].lines[1])
                startingLine = i
########################################################################################################################
            if(inLoopCondition and presentChar == ')'):
                parenthesisCounter = parenthesisCounter - 1
                if(parenthesisCounter == 0):
                    currentStatement += presentChar
                    if(debugMode) : print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                    notAddedYet = False
                    inLoopCondition = False
                    if(debugMode) : print("semiBC printing --> ", "end of loop_cond detected.")
                    newPentad = pentadStruct([pentadList[startingLine].lines[0], pentadList[i].lines[1]], currentStatement)  
                    for valuableLine in range(startingLine, i):
                        for existingRole in pentadList[valuableLine].roles:
                            newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                    output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            if(inLoopCondition and presentChar == '('):
                parenthesisCounter = parenthesisCounter + 1
########################################################################################################################
            if(nextChar): #because we need to test the char before "for" and the one after it too! (but that way of doing thing requires the elif depending on InLoopCondition to be placed BEFORE... meh!)
                if(not inLoopCondition and re.search(r'(?:\W|\0|^)for\s*?', pentadList[i].text[:j]) and re.match(r'(\(|\\|\0|$)', nextChar) and re.search(r'(?:\W|\0|^)for\s*?(?=(\(|\\|\0|$))', currentStatement)):
                    if(debugMode) : print("semiBC printing --> ", "begining of loop_cond detected.")
                    inLoopCondition = True
                    if(presentChar == '('):
                        if(debugMode) : print("semiBC printing --> ", "(avec par)")
                        parenthesisCounter = 1
                    else:
                        if(debugMode) : print("semiBC printing --> ", "(sans par)")
                        parenthesisCounter = 0
########################################################################################################################
            if(presentChar == '{'):
                if(debugMode) : print("semiBC printing --> ", "beg of block detected.")
                if(currentStatement != ""):
                    newPentad = pentadStruct([pentadList[startingLine].lines[0], pentadList[lineOfTheLastCharRead].lines[1]], currentStatement)  
                    for valuableLine in range(startingLine, i):
                        for existingRole in pentadList[valuableLine].roles:
                            newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                    output.append(newPentad)
                currentStatement = "{"
                if(debugMode) : print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([pentadList[i].lines[0], pentadList[i].lines[1]], currentStatement)  
                for valuableLine in range(startingLine, i):
                    for existingRole in pentadList[valuableLine].roles:
                        newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            if(presentChar == '}'):
                if(debugMode) : print("semiBC printing --> ", "end of block detected.")
                if(currentStatement != ""):
                    newPentad = pentadStruct([pentadList[startingLine].lines[0], pentadList[lineOfTheLastCharRead].lines[1]], currentStatement)  
                    for valuableLine in range(startingLine, i):
                        for existingRole in pentadList[valuableLine].roles:
                            newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                    output.append(newPentad)
                currentStatement = "}"
                if(debugMode) : print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([pentadList[i].lines[0], pentadList[i].lines[1]], currentStatement)  
                for existingRole in pentadList[i].roles:
                    newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            if(presentChar == ';' and not inLoopCondition):
                if(debugMode) : print("semiBC printing --> ", "\';\' detected outside of loop condition.")
                currentStatement += presentChar
                if(debugMode) : print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([pentadList[startingLine].lines[0], pentadList[i].lines[1]], currentStatement)  
                for valuableLine in range(startingLine, i):
                    for existingRole in pentadList[valuableLine].roles:
                        newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            elif(i == len(pentadList)-1 and j == len(pentadList[i].text)-1):
                if(debugMode) : print("semiBC printing --> ", "EOF detected.")
                #currentStatement += presentChar
                if(debugMode) : print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([pentadList[startingLine].lines[0], pentadList[i].lines[1]], currentStatement)  
                for valuableLine in range(startingLine, i):
                    for existingRole in pentadList[valuableLine].roles:
                        newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
            if(notAddedYet):
                if(not (presentChar == '\\' and currentStatement == "")): #that if is for "case 21}\[\n]22;" of testfileMultiLines 
                    currentStatement += presentChar
                    if(debugMode) : print("semiBC printing --> ", "char \'", presentChar, "\' added to", currentStatement)
            lineOfTheLastCharRead = i
    return spaceNormalizer(output, False)



def multiLineManager(pentadList = [], debugMode = False):
    """ Takes the complete list of pentads and returns this list once every multilines
    being put on a single line. That's ALL.
    """
    output = []
    currentStatement = ""
    presentChar = 'a'
    startingLine = 0
    i = 0
    state = "Nothing"
    for i in range (len(pentadList)):
        ########### Variables #############
        for j in range (len(pentadList[i].text)):
            presentChar = str(pentadList[i].text[j])
            if(debugMode) : print("MultiLM printing --> ", "j = ", j, " len = ", len(pentadList[i].text), "presentChar = ", presentChar)
            ##########################################
            if(currentStatement == ""):
                if(debugMode) : print("MultiLM printing --> ", "No char yet in the buffer")
                startingLine = i
            if(j == len(pentadList[i].text)-1):
                if(debugMode) : print("MultiLM printing --> ", "\'\\n\' detected.")
                state = "Store and Restart"
            if(presentChar != '\n' and presentChar != '\\' ):
                currentStatement += presentChar
                if(debugMode) : print("MultiLM printing --> ", "char \'", presentChar, "\' added to", currentStatement)
            if(presentChar == '\\'):
                if(currentStatement != ""):
                    currentStatement += " "
                if(debugMode) : print("MultiLM printing --> ", "char ", presentChar, "\' detected and replaced by space.") #to avoid the case "unsigned\int" becoming "unsignedint" for eg.
            if(state == "Store and Restart"):
                state = "Nothing"
                newPentad = pentadStruct([pentadList[startingLine].lines[0], pentadList[i].lines[1]], currentStatement)
                for roleOfPreviousLine in pentadList[i].roles:
                    newPentad.addRole(roleOfPreviousLine.type, roleOfPreviousLine.mainVar, roleOfPreviousLine.otherVars)
                output.append(newPentad)
                currentStatement = ""
    if(currentStatement != ""):
        output.append(pentadStruct([startingLine, i], currentStatement))            
    return spaceNormalizer(output, debugMode)


def doWhileConverter(pentadList = [], debugMode = False, executedManyTimes = 0):
    """The objective here is to convert do-while loops in for loops using regex."""
    executedManyTimes = executedManyTimes + 1
    if executedManyTimes == 15 : return []
    presentChar = 'a'
    firstChar = 'a'
    secondChar = 'a'
    thirdChar = 'a'
    i = 0
    j = 0
    doLine = 0
    doChar1 = 0
    doChar2 = 0
    endBracketLine = 0
    endBracketChar = 0
    doWhileCondition = ""
    doWhileConditionANDWhileKeyword = ""
    doWhileConditionANDWhileKeywordLine = 0
    recursiveCase = False
    bracketCounter = 0
    state = "Nothing"
    if(debugMode) : print("\nDOWHILE printing --> ", "Starting")
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #for lines that start directly with "do"
        for j in range (len(pentadList[i].text)):
            ########### Variables ####################
            #line = pentadList[i].text
            presentChar = pentadList[i].text[j]
            if(debugMode) : print("line = ", i, " | j =", j, " | len = ", len(pentadList[i].text), " | read : " , presentChar)
            if (j < len(pentadList[i].text)-1) : firstChar = pentadList[i].text[j+1]
            else: firstChar = None
            if (j < len(pentadList[i].text)-2) : secondChar = pentadList[i].text[j+2]
            else: secondChar = None
            if (j < len(pentadList[i].text)-3) : thirdChar = pentadList[i].text[j+3]
            else: thirdChar = None
            ##########################################
            if(state == "Nothing" and re.search(r'(?:\W|\0|^|\s)', str(presentChar)) and firstChar == 'd' and secondChar == 'o' and (thirdChar == None or re.search(r'(\W)', str(thirdChar))!=None)):
                if(debugMode) : print(re.search(r'\W|\0|$', str(thirdChar)))
                state = "Before Loop"
                doLine = i
                doChar1 = j+1
                doChar2 = j+2
                if(debugMode) : print("DOWHILE printing --> ", "do found : line", doLine, ", Char ", doChar1)
            elif(re.search(r'(?:\W|\0|^|\s)', str(presentChar)) and firstChar == 'd' and secondChar == 'o' and (thirdChar == None or re.search(r'(\W)', str(thirdChar))!=None)):
                if(debugMode) : print("DOWHILE printing --> ", "another do found : line", i, ", Char ", j)
                recursiveCase = True
            if(state == "Before Loop" and bracketCounter == 0 and presentChar == '{'):
                state = "Inside Loop"
                if(debugMode) : print("DOWHILE printing --> ", state)
                bracketCounter = 1
                #opBracketLine = i
                #opBracketChar = j
            elif(state == "Inside Loop" and bracketCounter != 0 and presentChar == '{'):
                bracketCounter = bracketCounter + 1
            if(state == "Inside Loop" and bracketCounter == 1 and presentChar == '}'):
                state = "After Loop"
                if(debugMode) : print("DOWHILE printing --> ", state, " with end_bracket at line ", i, " and at char ", j)
                bracketCounter = 0
                endBracketLine = i
                endBracketChar = j
            elif(state == "Inside Loop" and bracketCounter != 1 and presentChar == '}'):
                bracketCounter = bracketCounter - 1
            if(state == "After Loop" and re.search(r'(?<=\W)while[\\\s]*?(\(.*?\)[\\\s]*?;)', pentadList[endBracketLine].text[endBracketChar:])):
                state = "After condition"
                doWhileConditionANDWhileKeywordMatch = re.search(r'(?<=\W|\0)(?P<all>while[\\\s]*?(?P<cond>\(.*?\))[\\\s]*?;)', pentadList[i].text[endBracketChar:])
                doWhileCondition = doWhileConditionANDWhileKeywordMatch.group('cond')
                doWhileConditionANDWhileKeyword = doWhileConditionANDWhileKeywordMatch.group('all')
                doWhileConditionANDWhileKeywordLine = i
                if(debugMode) : print("DOWHILE printing --> ", "Match :", doWhileCondition)
                if(debugMode) : print("DOWHILE printing --> ", "That gonna be detroyed :", doWhileConditionANDWhileKeyword)
                pentadList[i].text = pentadList[i].text[:endBracketChar] + pentadList[i].text[endBracketChar:].replace(doWhileConditionANDWhileKeyword, "", 1)
                if(debugMode) : print("DOWHILE printing --> ", "After line :", pentadList[i].text)
                pentadList[doLine].text = pentadList[doLine].text[ : doChar1] \
                                        + "for" + doWhileCondition  \
                                        + pentadList[doLine].text[doChar2+1 : ]      
        
                pentadList[doWhileConditionANDWhileKeywordLine].addRole("while of do from line", str(doLine))
                break
        if(state == "After condition"):
            recursiveCase = True #we run the function one more time since we didnt analyse the entire code yet
            break
    if(recursiveCase):
        return doWhileConverter(pentadList, debugMode, executedManyTimes)


    return spaceNormalizer(pentadList)

def whileLoopConverter(pentadList = [], debugMode = False):
    """The objective here is to convert while loops in for loops using regex."""
    i = 0
    if(debugMode) : print("")
    for i in range (len(pentadList)):
        if(debugMode) : print("line = ", i, " | len = ", len(pentadList[i].text), " | read : " , pentadList[i].text)
        pattern = re.compile(r'(?P<char>\W|\0|^)while\s*(?=(\(|\\|\0|$))')
        found = re.search(pattern, pentadList[i].text)
        safetyBreakPoint = 0
        while(found != None):
            if(debugMode) : print ("found : " + found.group('char') + "while")
            if(debugMode) : print("line before : ", pentadList[i].text)
            pentadList[i].text = re.sub(pattern, found.group('char')+"for", pentadList[i].text, 1)
            if(debugMode) : print("line after  : ", pentadList[i].text)
            pattern = re.compile(r'(?P<char>\W|\0|^)while\s*(?=(\(|\\|\0|$))')
            found = re.search(pattern, pentadList[i].text)
            safetyBreakPoint = safetyBreakPoint + 1
            if safetyBreakPoint == 1000 : break
    return spaceNormalizer(pentadList)

def ifNormalizer(pentadList = [], debugMode = False):
    """The objective here is to convert do-while loops in for loops using regex."""
    if(debugMode) : print("\nIF printing --> ", "Starting")

    i = 0
    for i in range (len(pentadList)):
        pentadList[i].text = ' ' + pentadList[i].text #like always, it doesn't harm
        pattern = re.compile(r"""
        (?P<keyword> #########################################################
        (?:[\s]|[\\]|\0|^)+                                    # start of a keyword
        (?:if)                                                 # if
        (?:[\s]|[\\])*                                         # 0 or more spaces
        )
        (?P<condition> #########################################################
        (?:\()                                                 # an open parenthesis
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:[^\)\(])*?                                           # anything but a parenthesis or nothing
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:                                              #----------------------
        (?:\()                                           #     # a parenthesis
        (?:[\s]|[\\])*                                   #     # 0 or more spaces
        (?:[^\)\(])*?                                    #     # anything but a parenthesis or nothing
        (?:[\s]|[\\])*                                   #     # 0 or more spaces
        (?:\))                                           #     # a parenthesis
        )*                                               #------ 0 or more -----
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:[^\)\(])*?                                          # anything but a parenthesis or nothing
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:\))                                                 # a close parenthesis
        )
        (?P<instruction> #########################################################
        (?:[\s]|[\\])*                                         # 0 or more spaces
        (?:.)+?                                                # anything but lazy
        (?:[\s]|[\\])*                                         # 0 or more spaces
        )
        (?:;|$|\n|{)                                           # a semicolon or the end of line
        """, re.VERBOSE)
        if(re.search(pattern, pentadList[i].text)):
            found = re.findall(pattern, pentadList[i].text)
            for h in found :
                if(debugMode) : print("\nIF printing --> ", "st before = ", pentadList[i].text)
                pentadList[i].text = re.sub(pattern, h[0] + h[1] + ' { '+ h[2] +'; } ', pentadList[i].text)
                if(debugMode) : print("\nIF printing --> ", "st after = ", pentadList[i].text)
    return semicolonBasedChopper(pentadList, debugMode)


def elseNormalizer(pentadList = [], debugMode = False, executedManyTimes = 0):
    """The objective here is to convert do-while loops in for loops using regex."""
    executedManyTimes = executedManyTimes + 1
    if(executedManyTimes == 30) : return []
    presentChar = "//"
    memory1 = "//"
    memory2 = "//"
    memory3 = "//"
    memory4 = "//"
    memory5 = "//"
    mode = "nothing"
    bracketCounter = 0
    paranthesisCounter = 0
    lastElseFound = 0
    i = 0
    j = 0
    recursiveCase = False
    elseExpected = False
    doubt = "no doubt"
    if(debugMode) : print("\nELSE printing --> ", "Starting")
    while i < len(pentadList):
        if(i > 1500): break #safety in case of BS
        pentadList[i].text = ' ' + pentadList[i].text #for lines that start directly with "else"
        pentadList[i].text = ' ' + pentadList[i].text.replace(" else{", " else {")
        j = 0
        while j < len(pentadList[i].text):
            if(j > 1000): break #safety in case of BS
            ########### Variables ####################
            #line = pentadList[i].text
            memory1 = memory2
            memory2 = memory3
            memory3 = memory4
            memory4 = memory5
            memory5 = presentChar
            presentChar = pentadList[i].text[j]
            if(debugMode) : print("ELSE printing --> ", "line = ", i, "| read : " , presentChar, " | in memory : " , memory1, memory2, memory3, memory4, memory5)
            ########### Let's start ####################
            if(mode == "nothing" or mode == "closingLastElse"):
                if(presentChar == ' ' and memory1 == ' ' and memory2 == 'e' and memory3 == 'l' and memory4 == 's' and memory5 == 'e'):
                    if(mode == "nothing") :
                        mode = "readElse"
                        if(debugMode) : print("\nELSE printing --> ", "else detected : readElse mode activated !\n")
                    if(mode == "closingLastElse") :
                        mode = "readLastElse"
                        if(debugMode) : print("\nELSE printing --> ", "else detected : readLastElse mode activated !\n")
            if(mode == "readElse" or mode == "readLastElse"):
                if(presentChar != ' '):
                    if(debugMode) : print("\nELSE printing --> ", "A new char :", presentChar," has been read !")
                    if(presentChar == '{'):
                        if(debugMode) : print("\nELSE printing --> ", "Too bad... that's a brackety.")
                        if(mode == "readElse"):
                            mode = "readBracket"
                            if(debugMode) : print("\nELSE printing --> ", "readBracket mode activated !\n")
                        if(mode == "readLastElse") :
                            mode = "continuingInsideLastElse"
                            if(debugMode) : print("\nELSE printing --> ", "At this point, we already found an else, then checked if there was another one after that, then find the last one.")
                            if(debugMode) : print("\nELSE printing --> ", "And this else has an opening bracket. So we just need to wait until the closing one, and we're done !")
                            if(debugMode) : print("\nELSE printing --> ", "We just need to find the closing one and to add another closing bracket directly after it. That's all.")
                            if(debugMode) : print("\nELSE printing --> ", "continuingInsideLastElse mode activated !\n")
                            bracketCounter = 0
                            paranthesisCounter = 0
                    else:
                        if(mode == "readElse"):
                            mode = "somethingElseAfterElse"
                            if(debugMode) : print("\nELSE printing --> ", "somethingElseAfterElse mode activated !\n")
                        if(mode == "readLastElse"):
                            mode = "somethingAfterLastElse"
                            if(debugMode) : print("\nELSE printing --> ", "\nThat's a shame we can't take care of that now. We need to focus on closing the wrapping else.")
                            if(debugMode) : print("\nELSE printing --> ", "\nI guess we're good for another round once we're done.\n")
                            recursiveCase = True
                            if(debugMode) : print("\nELSE printing --> ", "somethingAfterLastElse mode activated !\n")
                            bracketCounter = 0
                            paranthesisCounter = 0
            elif(mode == "readBracket"):
                mode = "nothing"
                if(debugMode) : print("\nELSE printing --> ", "back to nothing mode !\n")
                bracketCounter = 0
                paranthesisCounter = 0
                lastElseFound = 0
                elseExpected = False
            if(mode == "continuingInsideLastElse"):
                if(recursiveCase == False and doubt == "no doubt" and (presentChar == ' ' and memory1 == ' ' and memory2 == 'e' and memory3 == 'l' and memory4 == 's' and memory5 == 'e')):
                    doubt = "small doubt"
                    memory5 = "/doubt/"
                if(doubt == "small doubt"):
                    if(memory1 == "/doubt/" or memory2 == "/doubt/" or memory3 == "/doubt/"):
                        if((presentChar == ' ' or presentChar == '(') and (memory3 == ' ' or memory3 == '//' or memory3 == ';' or memory3 == '}') and memory4 == 'i' and memory5 == 'f'):
                            if(debugMode) : print("\n\nELSE printing --> ", "That's official, we just found another if-else that needs to be handled !\n\n")
                            recursiveCase = True
                            doubt = "no doubt"
                if(presentChar == '('): paranthesisCounter += 1
                if(presentChar == ')'): paranthesisCounter -= 1
                if(presentChar == '{'): bracketCounter += 1
                if(presentChar == '}'):
                    bracketCounter -= 1
                    if(bracketCounter == 0):
                        if(debugMode) : print("\nELSE printing --> ", "And here it is. Damn was that long !")
                        if(debugMode) : print("\nELSE printing --> ", "line", i ,"before :", pentadList[i].text)
                        pentadList[i].text = pentadList[i].text[:j+1] + ' } ' + pentadList[i].text[j+1:] 
                        if(debugMode) : print("\nELSE printing --> ", "line", i ,"after :", pentadList[i].text)
                        j = j + 3
                        mode = "nothing"
                        if(debugMode) : print("\nELSE printing --> ", "back to nothing mode !\n")
                        bracketCounter = 0
                        paranthesisCounter = 0
                        lastElseFound = 0
                        elseExpected = False
            if(mode == "somethingElseAfterElse"):
                if(debugMode) : print("\nELSE printing --> ", "line", i ,"before :", pentadList[i].text)
                pentadList[i].text = pentadList[i].text[:j] + ' { ' + pentadList[i].text[j:] 
                if(debugMode) : print("\nELSE printing --> ", "line", i ,"after :", pentadList[i].text)
                j = j + 3
                mode = "opBracketAdded"
                bracketCounter = 0
                paranthesisCounter = 0
                if(debugMode) : print("\nELSE printing --> ", "opBracketAdded mode activated !\n")
                if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, "so we're looking for the next ';'\n")
            if(mode == "opBracketAdded" or mode == "somethingAfterLastElse"):
                if(bracketCounter == 0 and paranthesisCounter == 0): #keep before updating par. counter !
                    if((presentChar == ' ' or presentChar == '(') and (memory3 == ' ' or memory3 == '//' or memory3 == ';' or memory3 == '}') and memory4 == 'i' and memory5 == 'f'):
                        if(mode == "opBracketAdded") :
                            if(debugMode) : print("\nELSE printing --> ", "We just read an \"if\" keyword ! That means we might have a \"else\" somewhere later.\n")
                            elseExpected = True
                            if(debugMode) : print("\nELSE printing --> ", "elseExpected is now True !")
            if(mode == "opBracketAdded" or mode == "somethingAfterLastElse"):
                if(presentChar == '('): paranthesisCounter += 1
                if(presentChar == ')'): paranthesisCounter -= 1
                if(presentChar == '{'):
                    bracketCounter += 1
                    if(bracketCounter != 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, "so we're waiting to the end of that block !!\n")
                if(presentChar == '}'):
                    bracketCounter -= 1
                    if(bracketCounter != 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, "and we're still waiting...")
                    else:
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, "so that's it ! That's the end of our waiting.\n")
                if((presentChar == ';' or presentChar == '}') and bracketCounter == 0 and paranthesisCounter != 0):
                    if(debugMode) : print("\nELSE printing --> ", "That's a trap, we're inside a loop condition or something !")
                if((presentChar == ';' or presentChar == '}') and bracketCounter == 0 and paranthesisCounter == 0):
                    if(mode == "opBracketAdded"):
                        mode = "endOfBlockFound"
                        if(debugMode) : print("\nELSE printing --> ", "Yes !!! '", presentChar, "' detected : endOfBlockFound mode activated !\n")
                    if(mode == "somethingAfterLastElse"):
                        if(debugMode) : print("\nELSE printing --> ", "FINALY ! We should have included everything now I think.\n")
                        if(debugMode) : print("\nELSE printing --> ", "line", i ,"before :", pentadList[i].text)
                        pentadList[i].text = pentadList[i].text[:j+1] + ' } ' + pentadList[i].text[j+1:] 
                        if(debugMode) : print("\nELSE printing --> ", "line", i ,"after :", pentadList[i].text)
                        j = j + 3
                        mode = "nothing"
                        if(debugMode) : print("\nELSE printing --> ", "back to nothing mode !\n")
                        bracketCounter = 0
                        paranthesisCounter = 0
                        lastElseFound = 0
                        elseExpected = False
            if(mode == "endOfBlockFound"):
                if(elseExpected == False):
                    if(debugMode) : print("\nELSE printing --> ", "line", i ,"before :", pentadList[i].text)
                    pentadList[i].text = pentadList[i].text[:j+1] + ' } ' + pentadList[i].text[j+1:] 
                    if(debugMode) : print("\nELSE printing --> ", "line", i ,"after :", pentadList[i].text)
                    j = j + 3
                    mode = "nothing"
                    if(debugMode) : print("\nELSE printing --> ", "back to nothing mode !")
                if(elseExpected == True):
                    mode = "continuingToFindElse"
                    if(debugMode) : print("\nELSE printing --> ", "We're not done yet. Let's check if we can find an \"else\" after that...")
                    if(debugMode) : print("\nELSE printing --> ", "continuingToFindElse mode activated !\n")
            elif(mode == "continuingToFindElse"): # Warning ! else-if so we don't read the closing bracket or the semicolon again directly
                if( not (presentChar == ' ')
                and not (presentChar == 'e' and memory5 == ' ')
                and not (presentChar == 'l' and memory4 == ' ' and memory5 == 'e')
                and not (presentChar == 's' and memory3 == ' ' and memory4 == 'e' and memory5 == 'l')
                and not (presentChar == 'e' and memory2 == ' ' and memory3 == 'e' and memory4 == 'l' and memory5 == 's')
                and not (presentChar == ' ' and memory1 == ' ' and memory2 == 'e' and memory3 == 'l' and memory4 == 's' and memory5 == 'e')):
                    if(debugMode) : print("\nELSE printing --> ", "Meh ! That's no \"else\" at all. Let's insert a closing bracket and leave it.")
                    if(debugMode) : print("\nELSE printing --> ", "line", i ,"before :", pentadList[i].text)
                    pentadList[i].text = pentadList[i].text[:j] + ' } ' + pentadList[i].text[j:] 
                    if(debugMode) : print("\nELSE printing --> ", "line", i ,"after :", pentadList[i].text)
                    j = j + 1
                    mode = "nothing"
                    elseExpected = False
                    if(debugMode) : print("\nELSE printing --> ", "back to nothing mode !")
                if(presentChar == ' ' and memory1 == ' ' and memory2 == 'e' and memory3 == 'l' and memory4 == 's' and memory5 == 'e'):
                    if(debugMode) : print("\nELSE printing --> ", "Yiff !!! That's what we were looking for !")
                    if(debugMode) : print("\nELSE printing --> ", "But there is a chance that another else is waiting even further away...")
                    if(debugMode) : print("\nELSE printing --> ", "Here is what we're going to do : We gonna remember this statement.")
                    if(debugMode) : print("\nELSE printing --> ", "If, when we continue, we cannot find another \"else\" at our level")
                    if(debugMode) : print("ELSE printing --> ", "(before finding an \"if\" expression at our level ofc.), then we will")
                    if(debugMode) : print("ELSE printing --> ", "came back to this block and insert a closing bracket at the end of it.")
                    if(debugMode) : print("\nELSE printing --> ", "And if we found a new \"else\" statement, we're just going to repeat that !")
                    if(j > 1) : lastElseFound = i
                    else : lastElseFound = i-1
                    mode = "isThereAnotherElse"
                    if(debugMode) : print("\nELSE printing --> ", "isThereAnotherElse mode activated !\n")
                    presentChar = "/else/"
                    bracketCounter = 0
                    paranthesisCounter = 0
            elif(mode == "isThereAnotherElse"): # Warning ! else-if so we don't read "else" directly
                if(paranthesisCounter == 0 and bracketCounter == 0):
                    if(presentChar == ' ' and memory1 == ' ' and memory2 == 'e' and memory3 == 'l' and memory4 == 's' and memory5 == 'e'):
                        recursiveCase = True
                        if(debugMode) : print("\nELSE printing --> ", "That's an \"else\" ! I will remember this one instead of the other.")
                        if(debugMode) : print("\nELSE printing --> ", "And concerning the other one... We're gonna need another round once we're done I guess.\n")
                        lastElseFound = i
                        presentChar = "/else/"
                        continue
                    if(memory1 != "/else/" and memory2 != "/else/" and memory3 != "/else/"):
                        if((presentChar == ' ' or presentChar == '(') and (memory3 == ' ' or memory3 == '//' or memory3 == ';' or memory3 == '}') and memory4 == 'i' and memory5 == 'f'):
                            if(debugMode) : print("\nELSE printing --> ", "We just read an \"if\" keyword, so we don't have to wait for an \"else\" anymore !\n")
                            if(debugMode) : print("\nELSE printing --> ", "closingLastElse mode activated !\n")
                            mode = "closingLastElse"
                            i = lastElseFound
                            j = 0
                            continue
                if(presentChar == '('):
                    paranthesisCounter += 1
                    if(paranthesisCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "paranthesisCounter = ", paranthesisCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                    if(bracketCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                if(presentChar == ')'):
                    paranthesisCounter -= 1
                    if(paranthesisCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "paranthesisCounter = ", paranthesisCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                    if(bracketCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                    if(paranthesisCounter == 0 and bracketCounter == 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = 0 and paranthesisCounter = 0, so we're still waiting for an \"else\" or an \"if\"...\n")
                if(presentChar == '{'):
                    bracketCounter += 1
                    if(paranthesisCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "paranthesisCounter = ", paranthesisCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                    if(bracketCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                if(presentChar == '}'):
                    bracketCounter -= 1
                    if(paranthesisCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "paranthesisCounter = ", paranthesisCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                    if(bracketCounter > 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = ", bracketCounter, ". Even if we find an \"else\", it wouldn't be relevant.\n")
                    if(paranthesisCounter == 0 and bracketCounter == 0):
                        if(debugMode) : print("\nELSE printing --> ", "bracketCounter = 0 and paranthesisCounter = 0, so we're still waiting for an \"else\" or an \"if\"...\n")
            if(mode == "isThereAnotherElse" and i == len(pentadList)-1 and j == len(pentadList[i].text)-1):
                if(debugMode) : print("\nELSE printing --> ", "And here we are, at the end of the list. And the last \"else\" we read was on line", lastElseFound,".\n")
                if(debugMode) : print("\nELSE printing --> ", "closingLastElse mode activated !\n")
                mode = "closingLastElse"
                i = lastElseFound
                j = 0
                continue
            j = j + 1
        i = i + 1

    if(recursiveCase):
        pentadList = semicolonBasedChopper(pentadList, False)
        if(debugMode) : print("\n  _________ AND LET'S GO TO ANOTHER ROUND !_________  \n")
        if(debugMode) : printAllWithRoles(pentadList)
        if(debugMode) : print("\n  __________________________________________________  \n")
        return elseNormalizer(pentadList, debugMode, executedManyTimes)
    return semicolonBasedChopper(pentadList, debugMode)


    