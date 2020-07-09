from pentadClass import pentadStruct
import re

def spaceNormalizer(listOfEveryPentads = None):
    """Takes the list of all pentads and returns this list with the
    modified text elements so that unnecessary spaces are removed.
    
    The strings we manipulate come from the C language, but this
    language is not space sensitive, meaning that it is possible
    to add spaces anywhere in the code where it is already
    syntactically correct to find a single space. To simplify
    the analysis of the code, we will remove all multiple spaces
    by reducing them to a single space. """
    output = []
    #line = ""
    presentChar = 'a'
    nextChar = 'a'
    stringStatement = "Nothing"
    for i in range (len(listOfEveryPentads)):
        output.append(pentadStruct(listOfEveryPentads[i].line, ""))
        if (stringStatement == "Nothing") :
            listOfEveryPentads[i].text = listOfEveryPentads[i].text.lstrip() #remove every space before the first character
            #print("lstrip output[" + str(i) + "].text = |" + output[i].text + "|")
        for j in range (len(listOfEveryPentads[i].text)):
            ######################################
            #line = output[i].text
            presentChar = listOfEveryPentads[i].text[j]
            if (j < len(listOfEveryPentads[i].text)-1) :
                nextChar = listOfEveryPentads[i].text[j+1]
            else:
                nextChar = None
            ######################################
            if (stringStatement == "Nothing" and presentChar == "\"") :
                stringStatement = "Going"
            elif (stringStatement == "Going" and presentChar == "\"") :
                stringStatement = "Nothing"
            if (stringStatement == "Going" and presentChar != '\n') :
                output[i].text += listOfEveryPentads[i].text[j]
                #print("output[" + str(i) + "].text = |" + output[i].text + "|")
            elif (not (presentChar==" " and (nextChar == " " or nextChar == None or nextChar == "\n")) and presentChar != '\n'):
                output[i].text += listOfEveryPentads[i].text[j]
                #print("output[" + str(i) + "].text = |" + output[i].text + "|")
        if (stringStatement == "Nothing") :
            output[i].text.rstrip() #remove every space after the last character
            #print("rstrip output[" + str(i) + "].text = |" + output[i].text + "|")
            for role in listOfEveryPentads[i].role:
                output[i].addRole(role.type, role.mainVar, role.otherVars)
    return output

def commentsEraser(listOfEveryPentads = None):
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
    for i in range (len(listOfEveryPentads)):
        ########### Variables #############
        singleLineCommentDetected = False
        output.append(pentadStruct([i,i], ""))
        for j in range (len(listOfEveryPentads[i].text)):
            presentChar = listOfEveryPentads[i].text[j]
            if (j < len(listOfEveryPentads[i].text)-1) :
                nextChar = listOfEveryPentads[i].text[j+1]
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
                            #print("String ended line : " + str(i)) 
                        elif(listOfEveryPentads[i].text[j-1] != '\\'):
                            stringStatement = "Ended"
                            #print("String ended line : " + str(i)) 
                    elif(stringStatement == "Nothing") :
                        stringStatement = "Started"
                        #print("String started line : " + str(i))
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
                output[i].text += listOfEveryPentads[i].text[j]
                #print("Add " + presentChar)
    return spaceNormalizer(output)

def stringReducer(listOfEveryPentads = None):
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
    for i in range (len(listOfEveryPentads)):
        for j in range (len(listOfEveryPentads[i].text)):
            ########### Variables #############
            presentChar = listOfEveryPentads[i].text[j]
            if (j < len(listOfEveryPentads[i].text)-1) :
                nextChar = listOfEveryPentads[i].text[j+1]
            else:
                nextChar = None
            ##########################################
            #print("line = ", i, " | j =", j, " | len = ", len(listOfEveryPentads[i].text), " | read : " , presentChar)
            if(escapingChar == "Next one"):
                escapingChar = "This char"
            elif(escapingChar == "This char"):
                escapingChar = "No"
            if(presentChar == "\"" and escapingChar != "This char"):
                inAString = not inAString
                currentStatement += "\""
                #print("STRRED printing --> ", "char \' \" \' added to", currentStatement)
            elif(inAString):
                #print("STRRED printing --> ", "We're in a string, no char added")
                if(presentChar == '\\' and nextChar != '\n' ):
                    escapingChar = "Next one"
            else:
                currentStatement += presentChar
                #print("STRRED printing --> ", "char \'", presentChar, "\' added to", currentStatement)

        output.append(pentadStruct([i, i], currentStatement))
        currentStatement = ""    
    #output.append(pentadStruct([startingLine, i], currentStatement))            
    return spaceNormalizer(output)

def semicolonBasedChopper(listOfEveryPentads = None):
    """This function separates statement using ';' as a limitation point."""
    output = []
    currentStatement = ""
    presentChar = 'a'
    startingLine = 0
    inLoopCondition = False
    i = 0
    nextChar = None

    for i in range (len(listOfEveryPentads)):
        #print("line = ", i, " | len = ", len(listOfEveryPentads[i].text), " | read : " , listOfEveryPentads[i].text)
        pattern = re.compile(r'(?P<all>(\W|\0|^)for)(?=\()')
        found = re.search(pattern, listOfEveryPentads[i].text)
        safetyBreakPoint = 0
        while(found != None):
            #print ("found : " + found.group('all'))
            #print("line before : ", listOfEveryPentads[i].text)
            listOfEveryPentads[i].text = re.sub(pattern, found.group('all')+" ", listOfEveryPentads[i].text, 1)
            #print("line after  : ", listOfEveryPentads[i].text)
            pattern = re.compile(r'(?P<all>(\W|\0|^)for)(?=\()')
            found = re.search(pattern, listOfEveryPentads[i].text)
            safetyBreakPoint = safetyBreakPoint + 1
            if safetyBreakPoint == 1000 : break

    for i in range (len(listOfEveryPentads)):
        ########### Variables #############
        for j in range (len(listOfEveryPentads[i].text)):
            notAddedYet = True
            presentChar = listOfEveryPentads[i].text[j]
            if (j < len(listOfEveryPentads[i].text)-1) :
                nextChar = listOfEveryPentads[i].text[j+1]
            else:
                nextChar = None
            if(currentStatement == ""):
                #print("semiBC printing --> ", "No char yet in the buffer")
                startingLine = i
########################################################################################################################
            if(inLoopCondition and presentChar == ')'):
                parenthesisCounter = parenthesisCounter - 1
                if(parenthesisCounter == 0):
                    currentStatement += presentChar
                    #print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                    notAddedYet = False
                    inLoopCondition = False
                    #print("semiBC printing --> ", "end of loop_cond detected.")
                    newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)  
                    for valuableLine in range(startingLine, i):
                        for existingRole in listOfEveryPentads[valuableLine].role:
                            newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                    output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            if(inLoopCondition and presentChar == '('):
                parenthesisCounter = parenthesisCounter + 1
########################################################################################################################
            if(nextChar): #because we need to test the char before "for" and the one after it too! (but that way of doing thing requires the elif depending on InLoopCondition to be placed BEFORE... meh!)
                #print("semiBC printing --> ", "presentChar = ", presentChar, " and nextChar = ", nextChar)
                if(not inLoopCondition and re.search(r'(?:\W|\0|^)for\s*?', listOfEveryPentads[i].text[:j]) and re.match(r'(\(|\\|\0|$)', nextChar) and re.search(r'(?:\W|\0|^)for\s*?(?=(\(|\\|\0|$))', currentStatement)):
                    #print("semiBC printing --> ", "begining of loop_cond detected.")
                    inLoopCondition = True
                    if(presentChar == '('):
                        #print("semiBC printing --> ", "(avec par)")
                        parenthesisCounter = 1
                    else:
                        #print("semiBC printing --> ", "(sans par)")
                        parenthesisCounter = 0
########################################################################################################################
            if(presentChar == '{'):
                #print("semiBC printing --> ", "beg of loop detected.")
                if(currentStatement != ""):
                    newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)  
                    for valuableLine in range(startingLine, i):
                        for existingRole in listOfEveryPentads[valuableLine].role:
                            newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                    output.append(newPentad)
                currentStatement = "{"
                #print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)  
                for valuableLine in range(startingLine, i):
                    for existingRole in listOfEveryPentads[valuableLine].role:
                        newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            if(presentChar == '}'):
                #print("semiBC printing --> ", "end of loop detected.")
                if(currentStatement != ""):
                    newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)  
                    for valuableLine in range(startingLine, i):
                        for existingRole in listOfEveryPentads[valuableLine].role:
                            newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                    output.append(newPentad)
                currentStatement = "}"
                #print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)  
                for existingRole in listOfEveryPentads[i].role:
                    newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            if(presentChar == ';' and not inLoopCondition):
                #print("semiBC printing --> ", "\';\' detected outside of loop condition.")
                currentStatement += presentChar
                #print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)  
                for valuableLine in range(startingLine, i):
                    for existingRole in listOfEveryPentads[valuableLine].role:
                        newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
########################################################################################################################
            elif(i == len(listOfEveryPentads)-1 and j == len(listOfEveryPentads[i].text)-1):
                #print("semiBC printing --> ", "EOF detected.")
                currentStatement += presentChar
                #print("semiBC printing --> ", "specific char \'", presentChar, "\' added to", currentStatement)
                notAddedYet = False
                newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)  
                for valuableLine in range(startingLine, i):
                    for existingRole in listOfEveryPentads[valuableLine].role:
                        newPentad.addRole(existingRole.type, existingRole.mainVar, existingRole.otherVars)
                output.append(newPentad)
                currentStatement = ""
            if(notAddedYet):
                if(not (presentChar == '\\' and currentStatement == "")): #that if is for "case 21}\[\n]22;" of testfileMultiLines 
                    currentStatement += presentChar
                    #print("semiBC printing --> ", "char \'", presentChar, "\' added to", currentStatement)

    return spaceNormalizer(output)



def multiLineManager(listOfEveryPentads = None):
    """ Takes the complete list of pentads and returns this list once every multilines
    being put on a single line. That's ALL.
    """
    output = []
    currentStatement = ""
    presentChar = 'a'
    startingLine = 0
    i = 0
    state = "Nothing"
    for i in range (len(listOfEveryPentads)):
        ########### Variables #############
        for j in range (len(listOfEveryPentads[i].text)):
            presentChar = str(listOfEveryPentads[i].text[j])
            #print("MultiLM printing --> ", "j = ", j, " len = ", len(listOfEveryPentads[i].text), "presentChar = ", presentChar)
            ##########################################
            if(currentStatement == ""):
                #print("MultiLM printing --> ", "No char yet in the buffer")
                startingLine = i
            if(j == len(listOfEveryPentads[i].text)-1):
                #print("MultiLM printing --> ", "\'\\n\' detected.")
                state = "Store and Restart"
            if(presentChar != '\n' and presentChar != '\\' ):
                currentStatement += presentChar
                #print("MultiLM printing --> ", "char \'", presentChar, "\' added to", currentStatement)
            if(presentChar == '\\'):
                if(currentStatement != ""):
                    currentStatement += " "
                #print("MultiLM printing --> ", "char ", presentChar, "\' detected and replaced by space.") #to avoid the case "unsigned\int" becoming "unsignedint" for eg.
            if(state == "Store and Restart"):
                state = "Nothing"
                newPentad = pentadStruct([listOfEveryPentads[startingLine].line[0], listOfEveryPentads[i].line[1]], currentStatement)
                for roleOfPreviousLine in listOfEveryPentads[i].role:
                    newPentad.addRole(roleOfPreviousLine.type, roleOfPreviousLine.mainVar, roleOfPreviousLine.otherVars)
                output.append(newPentad)
                currentStatement = ""
    if(currentStatement != ""):
        output.append(pentadStruct([startingLine, i], currentStatement))            
    return spaceNormalizer(output)

def doWhileConverter(listOfEveryPentads = None):
    """The objective here is to convert do-while loops in for loops using regex."""
    presentChar = 'a'
    firstChar = 'a'
    secondChar = 'a'
    thirdChar = 'a'
    i = 0
    j = 0
    doLine = 0
    doChar1 = 0
    doChar2 = 0
    #opBracketLine = 0
    #opBracketChar = 0
    endBracketLine = 0
    endBracketChar = 0
    doWhileCondition = ""
    doWhileConditionANDWhileKeyword = ""
    doWhileConditionANDWhileKeywordLine = 0
    recursiveCase = False
    bracketCounter = 0
    state = "Nothing"
    #print("\nDOWHILE printing --> ", "Starting")
    for i in range (len(listOfEveryPentads)):
        listOfEveryPentads[i].text = ' ' + listOfEveryPentads[i].text #for lines that start directly with "do"
        for j in range (len(listOfEveryPentads[i].text)):
            ########### Variables ####################
            #line = listOfEveryPentads[i].text
            presentChar = listOfEveryPentads[i].text[j]
            #print("line = ", i, " | j =", j, " | len = ", len(listOfEveryPentads[i].text), " | read : " , presentChar)
            if (j < len(listOfEveryPentads[i].text)-1) : firstChar = listOfEveryPentads[i].text[j+1]
            else: firstChar = None
            if (j < len(listOfEveryPentads[i].text)-2) : secondChar = listOfEveryPentads[i].text[j+2]
            else: secondChar = None
            if (j < len(listOfEveryPentads[i].text)-3) : thirdChar = listOfEveryPentads[i].text[j+3]
            else: thirdChar = None
            ##########################################
            if(state == "Nothing" and re.search(r'(?:\W|\0|^)', str(presentChar)) and firstChar == 'd' and secondChar == 'o' and (thirdChar == None or re.search(r'(\W)', str(thirdChar))!=None)):
                #print(re.search(r'\W|\0|$', str(thirdChar)))
                state = "Before Loop"
                doLine = i
                doChar1 = j+1
                doChar2 = j+2
                #print("DOWHILE printing --> ", "do found : line", doLine, ", Char ", doChar1)
            elif(state == "Before Loop" and re.search(r'(?:\W|\0|^)', str(presentChar)) and firstChar == 'd' and secondChar == 'o' and (thirdChar == None or re.search(r'(\W)', str(thirdChar))!=None)):
                #print("DOWHILE printing --> ", "another do found : line", i, ", Char ", j)
                recursiveCase = True
            if(state == "Before Loop" and bracketCounter == 0 and presentChar == '{'):
                state = "Inside Loop"
                #print("DOWHILE printing --> ", state)
                bracketCounter = 1
                #opBracketLine = i
                #opBracketChar = j
            elif(state == "Inside Loop" and bracketCounter != 0 and presentChar == '{'):
                bracketCounter = bracketCounter + 1
            if(state == "Inside Loop" and bracketCounter == 1 and presentChar == '}'):
                state = "After Loop"
                #print("DOWHILE printing --> ", state, " with end_bracket at line ", i, " and at char ", j)
                bracketCounter = 0
                endBracketLine = i
                endBracketChar = j
            elif(state == "Inside Loop" and bracketCounter != 1 and presentChar == '}'):
                bracketCounter = bracketCounter - 1
            if(state == "After Loop" and re.search(r'(?<=\W)while[\\\s]*?(\(.*?\)[\\\s]*?;)', listOfEveryPentads[endBracketLine].text[endBracketChar:])):
                state = "After condition"
                doWhileConditionANDWhileKeywordMatch = re.search(r'(?<=\W|\0)(?P<all>while[\\\s]*?(?P<cond>\(.*?\))[\\\s]*?;)', listOfEveryPentads[i].text[endBracketChar:])
                doWhileCondition = doWhileConditionANDWhileKeywordMatch.group('cond')
                doWhileConditionANDWhileKeyword = doWhileConditionANDWhileKeywordMatch.group('all')
                doWhileConditionANDWhileKeywordLine = i
                #print("DOWHILE printing --> ", "Match :", doWhileCondition)
                #print("DOWHILE printing --> ", "That gonna be detroyed :", doWhileConditionANDWhileKeyword)
                listOfEveryPentads[i].text = listOfEveryPentads[i].text[:endBracketChar] + listOfEveryPentads[i].text[endBracketChar:].replace(doWhileConditionANDWhileKeyword, "", 1)
                #print("DOWHILE printing --> ", "After line :", listOfEveryPentads[i].text)
                listOfEveryPentads[doLine].text = listOfEveryPentads[doLine].text[ : doChar1] \
                                        + "for" + doWhileCondition  \
                                        + listOfEveryPentads[doLine].text[doChar2+1 : ]      
        
                listOfEveryPentads[doWhileConditionANDWhileKeywordLine].addRole("while of do from line", str(doLine))
                break
        if(state == "After condition"):
            recursiveCase = True #we run the function one more time since we didnt analyse the entire code yet
            break
    if(recursiveCase):
        
        return doWhileConverter(listOfEveryPentads)
    
    return spaceNormalizer(listOfEveryPentads)

def whileLoopConverter(listOfEveryPentads = None):
    """The objective here is to convert while loops in for loops using regex."""
    i = 0
    #print("")
    for i in range (len(listOfEveryPentads)):
        #print("line = ", i, " | len = ", len(listOfEveryPentads[i].text), " | read : " , listOfEveryPentads[i].text)
        pattern = re.compile(r'(?P<char>\W|\0|^)while\s*(?=(\(|\\|\0|$))')
        found = re.search(pattern, listOfEveryPentads[i].text)
        safetyBreakPoint = 0
        while(found != None):
            #print ("found : " + found.group('char') + "while")
            #print("line before : ", listOfEveryPentads[i].text)
            listOfEveryPentads[i].text = re.sub(pattern, found.group('char')+"for", listOfEveryPentads[i].text, 1)
            #print("line after  : ", listOfEveryPentads[i].text)
            pattern = re.compile(r'(?P<char>\W|\0|^)while\s*(?=(\(|\\|\0|$))')
            found = re.search(pattern, listOfEveryPentads[i].text)
            safetyBreakPoint = safetyBreakPoint + 1
            if safetyBreakPoint == 1000 : break
    return spaceNormalizer(listOfEveryPentads)