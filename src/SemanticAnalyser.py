from pentadClass import pentadStruct
from LexicalAnalyser import spaceNormalizer
import re
import sys

def mainSemanticalAnalyser(pentadList = [], criterionVariable = 'a', criterionLine = 20, debugMode = False):
    """This function calls every other functions in charge of the semantical analyser and contains
       the algo that handles the rules of this analysis. It takes as arguments the fully transformed
       list of PENTADs as well as the original slicing criterion, and returns the PENTADs list with
       usefulness of statements that belongs in the final slice changed to True."""
    criterionVariable = (spaceNormalizer([pentadStruct([0], criterionVariable)], False))[0].text #security for weird-ass variables
    if(len(pentadList) < 1):
        if(debugMode) : sys.exit(1)
        return [[], pentadList]
    if(debugMode) : print()
    if(debugMode) : print("——————————————————————————— SEMANTICAL ANALYSIS —————————————————————————")
    if(debugMode) : print()

    for o in range (len(pentadList)):
        pentadList[o].id = o           #id of a PENTAD = order in the list

    criterionStatement = findS1(pentadList, criterionLine, debugMode)
    pentadList = ultimateCodeBreaker(pentadList, criterionVariable, criterionStatement, debugMode)
    _____specialPrinter(pentadList, "At the very beginning", debugMode)

    

    targetList = [[criterionVariable, criterionStatement, "Other variable of an inside-else definition"]] #We'll consider this first statement as an inside-else definition
    i = 0
    while i < len(targetList):
        if(debugMode) : print("\nSL-SMA printing --> ", "Target List ", i+1, "/", len(targetList))
        if(debugMode) : print("SL-SMA printing --> ", "Variable : ", targetList[i][0], "   Statement ID :", targetList[i][1], "\n")
        quitter = False
        if(pentadList[targetList[i][1]].searchForRole("loopCondition")):
            if(debugMode) : print("\nSL-SMA printing --> ", "This statement is a loop condition.")
            for role in pentadList[targetList[i][1]].roles:
                if(role.type == "varDefine" and str(role.mainVar) == str(targetList[i][0])):
                    if(debugMode) : print("\nSL-SMA printing --> ", "We'll not search for previous definitions of this variable because it has already been defined in the loop condition")
                    quitter = True
                    break
        if (quitter == True): 
            i += 1
            continue

        idOfDeclaration = finderSliceDeclar(pentadList, targetList[i][0], targetList[i][1]-1, debugMode)
        if(idOfDeclaration != -1) : pentadList[idOfDeclaration].useful = True

        idOfLastDefinition = finderSliceDefine(pentadList, targetList[i][0], targetList[i][1]-1, debugMode)
        if(idOfLastDefinition != -1) : pentadList[idOfLastDefinition].useful = True

        #_____specialPrinter(pentadList, "Just after we found the definition", debugMode)

        if(pentadList[idOfLastDefinition].searchForRole("varDefine")):
            blockBegStatementId = findPossiblyContainingBlockOrigin(pentadList, idOfLastDefinition, debugMode)
            for othervariable in pentadList[idOfLastDefinition].searchForRole("varDefine").otherVars :
                if(pentadList[blockBegStatementId].searchForRole("elseBeg")) :
                    if(debugMode) : print("\nSL-SMA printing --> ", "This statement is indeed contained inside an else. Please, keep that in mind for later.\n")
                    targetList += [[othervariable, idOfLastDefinition, "Other variable of an inside-else definition"]]
                else : 
                    targetList += [[othervariable, idOfLastDefinition]]
                if(debugMode) : print("\nSL-SMA printing --> ", "Added : ", othervariable, " to targetList w/ st ", idOfLastDefinition, "\n")


        typeContainingBlock = "no type"
        blockBegStatementId = -2
        interestingStatementId = idOfLastDefinition

        while blockBegStatementId != -1 :

            if(blockBegStatementId == -2) :
                if(debugMode) : print("SL-SMA printing --> ", "Is statement n°", idOfLastDefinition, "contained in a block of instructions ? Maybe several blocks ?")
                if(debugMode) : print("SL-SMA printing --> ", "Just for you to remember, the text of this statement is \"", pentadList[idOfLastDefinition].text, "\".")

            blockBegStatementId = findPossiblyContainingBlockOrigin(pentadList, interestingStatementId, debugMode)

            if(blockBegStatementId == -1) :
                if(debugMode) : print("SL-SMA printing --> ", "There is no containing block over this point. No loops, nor if/else.")
                break
            else :
                pentadList[blockBegStatementId].useful = True #add beg to the slice
                if(pentadList[blockBegStatementId].searchForRole("loopBeg")) : typeContainingBlock = "loop"
                elif(pentadList[blockBegStatementId].searchForRole("ifBeg")) : typeContainingBlock = "if"
                elif(pentadList[blockBegStatementId].searchForRole("elseBeg")) : typeContainingBlock = "else"
                blockEndStatementId = findBlockEnd(pentadList, blockBegStatementId, typeContainingBlock, debugMode)
                if(blockEndStatementId != -1) : pentadList[blockEndStatementId].useful = True #add end to the slice

                if(blockBegStatementId > 0):
                    if((pentadList[blockBegStatementId].searchForRole("loopBeg") and pentadList[blockBegStatementId - 1].searchForRole("loopCondition"))    # Just to double check if the statement
                    or (pentadList[blockBegStatementId].searchForRole("ifBeg")   and pentadList[blockBegStatementId - 1].searchForRole("ifCondition")  )    # before the beg of the block is the 
                    or (pentadList[blockBegStatementId].searchForRole("elseBeg") and pentadList[blockBegStatementId - 1].searchForRole("elseCondition"))) : # condition of the block (loopCond or any)
                        blockCondStatement = blockBegStatementId - 1
                        pentadList[blockCondStatement].useful = True #add condition to the slice
                        interestingStatementId = blockCondStatement #it's that statement which is going to be used next time we search for wrapping block

                if(typeContainingBlock == "loop" or typeContainingBlock == "if") :
                    for role1 in pentadList[blockCondStatement].roles:
                        if(role1.type == "loopCondition" or role1.type == "ifCondition"):
                            for othervariable in role1.otherVars :
                                    varDeclarInLoopCond = False
                                    for role2 in pentadList[blockCondStatement].roles:
                                        if(role2.type == "varDeclar" and role2.mainVar == othervariable):
                                            varDeclarInLoopCond = True
                                    if(not varDeclarInLoopCond):
                                        if(debugMode) : print("SL-SMA printing --> ", "The condition for this block is \"", pentadList[blockCondStatement].text, "\".")
                                        if(debugMode) : print("SL-SMA printing --> ", othervariable, "has an influence over this condition. We add", othervariable, "to the targetList with this statement n°", blockCondStatement)
                                        if([othervariable, blockCondStatement] not in targetList and [othervariable, blockCondStatement, "Other variable of an inside-else definition"] not in targetList) :
                                            targetList += [[othervariable, blockCondStatement]] #only for loops and if : add <othervariable, loopcond/ifcond> to target list

                                    targetAlreadyHandled = False                                                        # Just to be sure that we didnt already search for
                                    for oldTargets in targetList:                                                       # redifinition of THIS variable in THIS loop.
                                        if(oldTargets[0] == othervariable and oldTargets[1] == blockEndStatementId):    # If we don't check, an infinite loop can happen.
                                            targetAlreadyHandled = True                                                 
                                    
                                    if(not targetAlreadyHandled and typeContainingBlock == "loop"):
                                        if(debugMode) : print("\nSL-SMA printing --> ", othervariable, "value could possibly be changed inside the body of the loop as well.")
                                        if([othervariable, blockEndStatementId] not in targetList and [othervariable, blockEndStatementId, "Other variable of an inside-else definition"] not in targetList) :
                                            targetList += [[othervariable, blockEndStatementId]]
                                            if(debugMode) : print("\nSL-SMA printing --> ", "Therefore, we're going to add ", othervariable, "to targetList starting from the closing bracket of that loop, at statement n°", blockEndStatementId, "\n") #only for loops : add <othervariable, loopend> to target list
                                        else :
                                            if(debugMode) : print("SL-SMA printing --> ", "Fortunately,", othervariable, "is already in the targetList with statement", blockEndStatementId, "\n")

                if(typeContainingBlock == "else") :
                    associatedIf = findPreviousIf(pentadList, blockCondStatement, debugMode)
                    if(associatedIf != [-1, -1, -1]):
                        associatedIfCond = associatedIf[0]
                        associatedIfBeg = associatedIf[1]
                        associatedIfEnd = associatedIf[2]
                        pentadList[associatedIfCond].useful = True
                        pentadList[associatedIfBeg].useful = True
                        pentadList[associatedIfEnd].useful = True

                        for role3 in pentadList[associatedIfCond].roles:
                            if(role3.type == "ifCondition"):
                                for othervariable in role3.otherVars :
                                    if(debugMode) : print("SL-SMA printing --> ", "The condition for this block is \"", pentadList[associatedIfCond].text, "\".")
                                    if(debugMode) : print("SL-SMA printing --> ", othervariable, "has an influence over this condition.")
                                    if([othervariable, associatedIfCond] not in targetList and [othervariable, associatedIfCond, "Other variable of an inside-else definition"] not in targetList) :
                                        targetList += [[othervariable, associatedIfCond]] #for that if : add <othervariable, loopcond/ifcond> to target list
                                        if(debugMode) : print("SL-SMA printing --> ", "We add", othervariable, "to the targetList with this statement n°", associatedIfCond)
                                    else :
                                        if(debugMode) : print("SL-SMA printing --> ",  othervariable, " is already in the targetList with statement", associatedIfCond, "\n")

                        targetAlreadyHandled = False                                                        # Just to be sure that we didnt already search for
                        for oldTargets in targetList:                                                       # redifinition of THIS variable in THIS if block.
                            if(oldTargets[0] == othervariable and oldTargets[1] == associatedIfEnd):        # If we don't check, it's not too bad, but it's better
                                targetAlreadyHandled = True                                                 # to optimize when we can.
                        
                        if(not targetAlreadyHandled and not pentadList[idOfLastDefinition].searchForRole("loopCondition") and len(targetList[i]) == 2):
                            if(debugMode) : print("\nSL-SMA printing --> ", "Even if we added a definition of variable", targetList[i][0], "to our slice, there is a chance that it will never be executed.")
                            if(debugMode) : print("SL-SMA printing --> ", "if the program runs the if starting at statement n°", associatedIfBeg, "we will never read the statement contained inside the else block.\n")
                            if(debugMode) : print("SL-SMA printing --> ", "Therefore, we add", targetList[i][0], "to targetList starting from the closing bracket of the if condition, at statement n°", associatedIfEnd, "\n") # for this if only : add <the variable that bring us here, ifend> to target list
                            if([targetList[i][0], associatedIfEnd] not in targetList and [othervariable, associatedIfEnd, "Other variable of an inside-else definition"] not in targetList) :
                                targetList += [[targetList[i][0], associatedIfEnd]]
                            else :
                                if(debugMode) : print("SL-SMA printing --> ", "In fact,",  targetList[i][0], " is already in the targetList with statement", associatedIfEnd, "\n")
                    

        i += 1

    _____specialPrinter(pentadList , "Just before return", debugMode)
    return pentadList


def ultimateCodeBreaker(pentadList = [], criterionVariable = "a", criterionStatement = 10000, debugMode = False):
    if(pentadList == []) : return -1
    blockBegStatementId = findPossiblyContainingBlockOrigin(pentadList, criterionStatement, debugMode)
    if(blockBegStatementId == -1) :
        if(debugMode) : print("SL-UCB printing --> ", "The criterion line of the slice is not contained inside an else.")
    elif(pentadList[blockBegStatementId].searchForRole("elseBeg")) :
        associatedIf = findPreviousIf(pentadList, blockBegStatementId - 1, debugMode)
        if(associatedIf != [-1, -1, -1]):
            associatedIfCond = associatedIf[0]
            associatedIfBeg = associatedIf[1]
            associatedIfEnd = associatedIf[2]
        for insideIf in range (associatedIfBeg+1, associatedIfEnd) :
            pentadList[insideIf].text = "//cannot be executed//"
            for role in pentadList[insideIf].roles :
                role.type = "Unexecutable"
    return pentadList







def findS1(pentadList = [], criterionLine = 10000, debugMode = False):
    """Takes a line number and returns the id of the statement that covers this line.
    If several statements do so, returns the highest id among these."""
    if(pentadList == []) : return -1
    S1 = 0
    i = 0
    for i in range (len(pentadList)):
        if(pentadList[i].lines[0] <= criterionLine):
            S1 = i
    if(debugMode) : print("SL-FS1 printing --> ", "Starting statement id is n°", pentadList[S1].id, ": \"", pentadList[S1].text, "\", covering lines", pentadList[S1].lines[0], "to", pentadList[S1].lines[1])      
    return S1

def finderSliceDeclar(pentadList = [], criterionVariable = "a", criterionStatement = None, debugMode = False):
    """Takes an element of the targetList (var, line) and returns the last id of the statement that
    has the role of variable declaration for this element."""
    if(pentadList == []) : return -1
    if(debugMode) : print("SL-DEC printing --> ", "Searchin the declaration of variable", criterionVariable, "from statement n°", criterionStatement)
    i = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in pentadList[i].roles :
            #if(debugMode) : print("SL-DEC printing --> ", "st :", i, "| lines :", pentadList[i].lines, "| role :", h.type, "| mainVar :", h.mainVar, "| var to search :", criterionVariable)
            if(h.type == "varDeclar" and h.mainVar == criterionVariable) :
                if(debugMode) : print("SL-DEC printing --> ", "Previous declaration statement id for variable", criterionVariable, "is n°", pentadList[i].id, ": \"", pentadList[i].text, "\", covering lines", pentadList[i].lines[0], "to", pentadList[i].lines[1])      
                return i
    if(debugMode) : print("SL-DEC printing --> ", "Previous declaration of variable", criterionVariable, "is nowhere to be found.")
    return -1
    
def finderSliceDefine(pentadList = [], criterionVariable = "a", criterionStatement = None, debugMode = False):
    """Takes an element of the targetList (var, line) and returns the last id of the statement that
    has the role of variable definition for this element."""
    if(pentadList == []) : return -1
    i = 0
    listOfIgnored = []
    elseCount = 1
    ignoration = "not"
    uUUUUuuuWWWyoumeanTHATif = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)

        if(ignoration == "not"):
            for h in pentadList[i].roles :
                if(h.type == "elseBeg") : elseCount = elseCount - 1
                if(h.type == "elseEnd") : elseCount = elseCount + 1
                if(elseCount == 0) :
                    ignoration = "else detected"

        if(ignoration == "else detected") :
            for h in pentadList[i].roles :
                if(h.type == "ifEnd") :
                    ignoration = "if to ignore"
                    uUUUUuuuWWWyoumeanTHATif = h.mainVar

        if(ignoration == "if to ignore") :
            for h in pentadList[i].roles :
                if(h.type == "ifCondition" and i == int(uUUUUuuuWWWyoumeanTHATif)) :  #doublechecking with condition id (and we're forced to cast int, of course...)
                    ignoration = "if ended"
            if(ignoration != "if ended") :listOfIgnored += [i]
        
        if(ignoration == "if ended") :
            elseCount = 1
            ignoration = "not"

    if(debugMode) : print("SL-DEF printing --> ","listOfIgnored :", listOfIgnored)

    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in pentadList[i].roles :
            #if(debugMode) : print("SL-DEF printing --> ", "st :", i, "| lines :", pentadList[i].lines, "| role :", h.type, "| mainVar :", h.mainVar, "| var to search :", criterionVariable)
            if(h.type == "varDefine" and h.mainVar == criterionVariable and not i in listOfIgnored) :
                if(debugMode) : print("SL-DEF printing --> ", "Previous definition statement id for variable", criterionVariable, "is n°", pentadList[i].id, ": \"", pentadList[i].text, "\", covering lines", pentadList[i].lines[0], "to", pentadList[i].lines[1])      
                return i
    if(debugMode) : print("SL-DEF printing --> ", "Previous definition of variable", criterionVariable, "is nowhere to be found.")
    return -1

def findPossiblyContainingBlockOrigin(pentadList = [], idOfPossiblyContainedStatement = 0, debugMode = False):
    """Takes the id of a statement and try to find a begLoop, a begIf or a begElse before this statement that would indicate that the 
    statement is contained inside a block. If it is found, it returns the id of the statement. Else, it returns -1."""
    if(debugMode) : print("SL-BEG printing --> ", "Searchin a wrapping block for statement n°", idOfPossiblyContainedStatement)
    if(idOfPossiblyContainedStatement == False) : return -1
    i = 0
    loopCount = 1
    ifCount = 1
    elseCount = 1
    for i in range (idOfPossiblyContainedStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in pentadList[i].roles :
            if(h.type == "loopBeg") : loopCount = loopCount - 1
            if(h.type == "loopEnd") : loopCount = loopCount + 1
            if(h.type == "ifBeg") : ifCount = ifCount - 1
            if(h.type == "ifEnd") : ifCount = ifCount + 1
            if(h.type == "elseBeg") : elseCount = elseCount - 1
            if(h.type == "elseEnd") : elseCount = elseCount + 1
            if(loopCount == 0) :
                if(debugMode) : print("SL-BEG printing --> ", "This statement is indeed contained inside a loop. This loop starts at statement n°", i)
                return i
            if(ifCount == 0) :
                if(debugMode) : print("SL-BEG printing --> ", "This statement is indeed contained inside an if. This if starts at statement n°", i) 
                return i
            if(elseCount == 0) :
                if(debugMode) : print("SL-BEG printing --> ", "This statement is indeed contained inside an else. This else starts at statement n°", i)
                return i
    return -1

def findBlockEnd(pentadList = [], idOfBlockOrigin = 0, blockType = "no type", debugMode = False):
    """Takes the id of a statement that has for role ifBeg, elseBeg or loopBeg and try to find the corresponding ending bracket.
    If it is found, it returns the id of the statement. Else, it returns -1."""
    if(idOfBlockOrigin == -1 or pentadList == []) : return -1
    if(debugMode) : print("SL-END printing --> ", "Searchin ending for that", blockType, "block that starts at statement n°", idOfBlockOrigin)
    whatWeSearch = "nothing"
    theOtherBracket = "nothing"
    searchCount = 1
    if (blockType == "loop"):
        whatWeSearch = "loopEnd"
        theOtherBracket = "loopBeg"
    if (blockType == "if"):
        whatWeSearch = "ifEnd"
        theOtherBracket = "ifBeg"
    if (blockType == "else"):
        whatWeSearch ="elseEnd"
        theOtherBracket = "elseBeg"
    i = 0
    for i in range (idOfBlockOrigin + 1, len(pentadList)):
        for h in pentadList[i].roles :
            if(h.type == whatWeSearch) :
                searchCount = searchCount - 1
            if(h.type == theOtherBracket) :
                searchCount = searchCount + 1
            if(searchCount == 0) :
                if(debugMode) : print("SL-END printing --> ", "The end of that block is statement n°", i)
                return i
    return -1


def findPreviousIf(pentadList = [], idOfElseStatement = 0, debugMode = False):
    """Takes the id of an else statement and try to find the begIf, the endIf and ifCond before this statement. 
    If it is found, it returns them all as [ifCond id, begIf id, endIf id]. Else, it returns [-1, -1, -1]."""
    if(debugMode) : print("\nSL-PIF printing --> ", "Searchin the associated if statement for else statement (n°", idOfElseStatement, ")")
    if(pentadList == [] or idOfElseStatement == 0) : return [-1, -1, -1]
    endIf = 0
    begIf = 0
    condIf = 0
    i = 0
    stopEverything = False
    for i in range (idOfElseStatement - 1, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        if(stopEverything) : break
        for h in pentadList[i].roles :
            if(h.type == "ifEnd") :
                endIf = i
                if(debugMode) : print("SL-PIF printing --> ", "That \"if\" block does exists, and it ends at statement n°", endIf)
                stopEverything = True
                break 
    i = 0
    stopEverything = False
    ifCount = 1
    for i in range (endIf - 1, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        if(stopEverything) : break
        for h in pentadList[i].roles :
            if(h.type == "ifBeg") : ifCount = ifCount - 1
            if(h.type == "ifEnd") : ifCount = ifCount + 1
            if(ifCount == 0) :
                begIf = i
                if(debugMode) : print("SL-PIF printing --> ", "That \"if\" blocks starts at statement n°", begIf) 
                stopEverything = True
                break 
    if(pentadList[begIf - 1].searchForRole("ifCondition")):
        condIf = begIf - 1
        if(debugMode) : print("SL-PIF printing --> ", "And obviously the if condition is in statement n°", condIf) 
        return [condIf, begIf, endIf]
    return [-1, -1, -1]



def _____specialPrinter(pentadList = [], msg = "", debugMode = False):
        msg2 = "----------------- "
        if(debugMode) : print("\n----------------- ", msg ," -----------------")
        for o in range (len(pentadList)):
            if pentadList[o].useful :
                if(debugMode) : print(o, ".\t", "--> " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
            else :
                if(debugMode) : print(o, ".\t", "    " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
        for c in msg : msg2 += "-"
        msg2 += " -----------------"
        if(debugMode) : print(msg2 + "\n")
