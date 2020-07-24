from pentadClass import pentadStruct
from LexicalAnalyser import spaceNormalizer
import re

def mainSemanticalAnalyser(pentadList = [], criterionVariable = 'a', criterionLine = 20, debugMode = False):
    """This function calls every other functions in charge of the semantical analyser and contains
       the algo that handles the rules of this analysis. It takes as arguments the fully transformed
       list of PENTADs as well as the original slicing criterion, and returns the PENTADs list with
       usefulness of statements that belongs in the final slice changed to True."""
    if(debugMode) : print()
    if(debugMode) : print("——————————————————————————— SEMANTICAL ANALYSIS —————————————————————————")
    if(debugMode) : print()
    for o in range (len(pentadList)):
        pentadList[o].id = o           #id of a PENTAD = order in the list
    if(debugMode) : print("\n----------------- At the very beginning -----------------")
    for o in range (len(pentadList)):
        if pentadList[o].useful :
            if(debugMode) : print(o, ".\t", "--> " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
        else :
            if(debugMode) : print(o, ".\t", "    " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
    if(debugMode) : print("------------------- ----------------- ------------------\n")

    criterionStatement = findS1(pentadList, criterionLine, debugMode)
    #pentadList[criterionStatement].useful = True
    if(debugMode) : print("\n----------------- Just after findS1 -----------------")
    for o in range (len(pentadList)):
        if pentadList[o].useful :
            if(debugMode) : print(o, ".\t", "--> " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
        else :
            if(debugMode) : print(o, ".\t", "    " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
    if(debugMode) : print("-------------------- ---------------- -----------------\n")
    targetList = [[criterionVariable, criterionStatement]]
    i = 0
    while i < len(targetList):
        if(debugMode) : print("\nWe progress through targetList (i =", i, ", len =", len(targetList), ")")
        if(debugMode) : print("\ncouple = [var =", targetList[i][0], ", st =", targetList[i][1], "]\n")
        idOfDeclaration = finderSliceDeclar(pentadList, targetList[i][0], targetList[i][1]-1, debugMode)
        if(idOfDeclaration != -1) : pentadList[idOfDeclaration].useful = True
        ###
        if(debugMode) : print("\n----------------- Just after we found the declaration -----------------")
        for o in range (len(pentadList)):
            if pentadList[o].useful :
                if(debugMode) : print(o, ".\t", "--> " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
            else :
                if(debugMode) : print(o, ".\t", "    " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
        if(debugMode) : print("-------------------- ----------------------------- -----------------\n")
        ###
        idOfDefinition = finderSliceDefine(pentadList, targetList[i][0], targetList[i][1]-1, debugMode)
        ###
        if(debugMode) : print("\n-----------------DDD-----------------")
        for o in range (len(pentadList)):
            if pentadList[o].useful :
                if(debugMode) : print(o, ".\t", "--> " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
            else :
                if(debugMode) : print(o, ".\t", "    " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
        if(debugMode) : print("-------------------------------------\n")
        ###
        for role in pentadList[idOfDefinition].roles:
            if(role.type == "varDefine"):
                for othervariable in role.otherVars :
                    targetList += [[othervariable, idOfDefinition]]
                    if(debugMode) : print("\nAdded : ", othervariable, " to targetList w/ st ", idOfDefinition)
        if(idOfDefinition != -1) : pentadList[idOfDefinition].useful = True
        isThisStatementInALoop = idOfDefinition
        begLoopStatement = -2
        endLoopStatement = -2
        loopCondStatement = -2
        while(begLoopStatement != -1 and endLoopStatement != -1 and loopCondStatement != -1):
            result = finderSliceLoop(targetList, pentadList, isThisStatementInALoop, debugMode)
            if(debugMode) : print("Result of finderSliceLoop is : ", result)
            begLoopStatement = result[0]
            endLoopStatement = result[1]
            loopCondStatement = result[2]
            if(begLoopStatement != -1):
                pentadList[begLoopStatement].useful = True
            if(endLoopStatement != -1):
                pentadList[endLoopStatement].useful = True
            if(loopCondStatement != -1):
                ###
                if(debugMode) : print("\n-----------------Inside loopCondStatement != -1-----------------")
                for o in range (len(pentadList)):
                    if pentadList[o].useful :
                        if(debugMode) : print(o, ".\t", "--> " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
                    else :
                        if(debugMode) : print(o, ".\t", "    " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
                if(debugMode) : print("-------------------------------------------------------------------")
                ###
                pentadList[loopCondStatement].useful = True
                for role1 in pentadList[loopCondStatement].roles:
                    if(role1.type == "loopCondition"):
                        for othervariable in role1.otherVars :
                            varDeclarOfVarInLoopCond = False
                            for role2 in pentadList[loopCondStatement].roles:
                                if(role2.type == "varDeclar" and role2.mainVar == othervariable):
                                    varDeclarOfVarInLoopCond = True
                            if(not varDeclarOfVarInLoopCond):
                                if(debugMode) : print("\nAdded : ", othervariable, " to targetList w/ st ", loopCondStatement)
                                targetList += [[othervariable, loopCondStatement]]
                            targetAlreadyHandled = False
                            for oldTargets in targetList:
                                if(oldTargets[0] == othervariable and oldTargets[1] == endLoopStatement):
                                    targetAlreadyHandled = True
                            if(not targetAlreadyHandled):
                                if(debugMode) : print("\nAdded : ", othervariable, " to targetList w/ st ", endLoopStatement)
                                targetList += [[othervariable, endLoopStatement]]
            isThisStatementInALoop = loopCondStatement
        i += 1
        ###
        if(debugMode) : print("----------------- Just before return -----------------")
        for o in range (len(pentadList)):
            if pentadList[o].useful :
                if(debugMode) : print(o, ".\t", "--> " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
            else :
                if(debugMode) : print(o, ".\t", "    " + str(pentadList[o].lines) + ".   " + pentadList[o].text)
        if(debugMode) : print("----------------- ------------------ -----------------")
        ###
    return pentadList

def findS1(listOfEveryPentads = None, criterionLine = 9, debugMode = False):
    """Takes a line number and returns the id of the statement that covers this line.
    If several statements do so, returns the highest id among these."""
    S1 = 0
    i = 0
    for i in range (len(listOfEveryPentads)):
        if(debugMode) : print("SL-fS1 printing --> ", "st ", listOfEveryPentads[i].id, ": ", listOfEveryPentads[i].text, " \t---\t ", listOfEveryPentads[i].lines[1], " - ", listOfEveryPentads[i].lines[0])      
        if(listOfEveryPentads[i].lines[0] <= criterionLine):
            S1 = i
    return S1

def finderSliceDeclar(listOfEveryPentads = None, criterionVariable = "a", criterionStatement = None, debugMode = False):
    """Takes an element of the targetList (var, line) and returns the last id of the statement that
    has the role of variable declaration for this element."""
    i = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].roles :
            if(debugMode) : print("SL-DEC printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].lines, "| role :", h.type, "| mainVar :", h.mainVar, "| var to search :", criterionVariable)
            if(h.type == "varDeclar" and h.mainVar == criterionVariable) :
                if(debugMode) : print("SL-DEC printing --> ", "here")
                return i
    if(debugMode) : print("SL-DEC printing --> ", "nowhere")
    return -1
    
def finderSliceDefine(listOfEveryPentads = None, criterionVariable = "a", criterionStatement = None, debugMode = False):
    """Takes an element of the targetList (var, line) and returns the last id of the statement that
    has the role of variable definition for this element."""
    i = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].roles :
            if(debugMode) : print("SL-DEF printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].lines, "| role :", h.type, "| mainVar :", h.mainVar, "| var to search :", criterionVariable)
            if(h.type == "varDefine" and h.mainVar == criterionVariable) :
                if(debugMode) : print("SL-DEF printing --> ", "here")
                return i
    if(debugMode) : print("SL-DEC printing --> ", "nowhere")
    return -1

def finderSliceLoop(targetList = [], listOfEveryPentads = None, sn_idB = 0, debugMode = False):
    """Takes the id of a statement and try to find a begLoop before this statement.
    If a begLoop is found, then search for the endLoop, then search for the loopCond,
    then return the three of them"""
    if(debugMode) : print("\nSL-LOO printing --> ", "Searchin loop for statement :", sn_idB)
    if(sn_idB == False) : return [-1, -1, -1]
    i = 0
    loopCount = 1
    begLoopStatement = -1
    endLoopStatement = -1
    loopCondStatement = -1
    for i in range (sn_idB, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].roles :
            if(h.type == "loopBeg") : loopCount = loopCount - 1
            if(h.type == "loopEnd") : loopCount = loopCount + 1
            if(loopCount == 0 and begLoopStatement == -1) :
                listOfEveryPentads[i].useful = True
                begLoopStatement = i
                if(debugMode) : print("SL-LOO printing --> ", "begLoop found at statement :", begLoopStatement)
    if(begLoopStatement == -1):
        return [-1, -1, -1]
    else :
        i = 0
        loopCount = 1
        for i in range (begLoopStatement + 1, len(listOfEveryPentads)): #incremental for loop to find the endLoop
            for h in listOfEveryPentads[i].roles :
                if(h.type == "loopBeg") : loopCount = loopCount + 1
                if(h.type == "loopEnd") : loopCount = loopCount - 1
                if(loopCount == 0 and endLoopStatement == -1) :
                    listOfEveryPentads[i].useful = True
                    endLoopStatement = i
                    if(debugMode) : print("SL-LOO printing --> ", "endLoop found at statement :", endLoopStatement)
        i = 0
        for i in range (begLoopStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
            for h in listOfEveryPentads[i].roles :
                if(h.type == "loopCondition" and loopCondStatement == -1) :
                    listOfEveryPentads[i].useful = True
                    loopCondStatement = i
                    if(debugMode) : print("SL-LOO printing --> ", "and here is the loop condition :", loopCondStatement)
                    # then add other variables to target list I guess...
    return [begLoopStatement, endLoopStatement, loopCondStatement]
        


