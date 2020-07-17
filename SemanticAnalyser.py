from pentadClass import pentadStruct
from LexicalAnalyser import spaceNormalizer
import re

def findS1(listOfEveryPentads = None, criterionLine = 9):
    """Takes a line number and returns the id of the statement that covers this line.
    If several statements do so, returns the highest id among these."""
    S1 = 0
    i = 0
    for i in range (len(listOfEveryPentads)):
#        print("SL-fS1 printing --> ", "st ", listOfEveryPentads[i].id, ": ", listOfEveryPentads[i].text, " \t---\t ", listOfEveryPentads[i].lines[1], " - ", listOfEveryPentads[i].lines[0])      
        if(listOfEveryPentads[i].lines[0] <= criterionLine):
            S1 = i
    return S1


def finderSliceDeclar(listOfEveryPentads = None, criterionVariable = "a", criterionStatement = None):
    """Takes an element of the targetList (var, line) and returns the last id of the statement that
    has the role of variable declaration for this element."""
    i = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].roles :
            #print("SL-DEC printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].lines, "| role :", h.type, "| mainVar :", h.mainVar)
            if(h.type == "varDeclar" and h.mainVar == criterionVariable) :
                #print("SL-DEC printing --> ", "here")
                return i
    return False
    
def finderSliceDefine(listOfEveryPentads = None, criterionVariable = "a", criterionStatement = None):
    """Takes an element of the targetList (var, line) and returns the last id of the statement that
    has the role of variable definition for this element."""
    i = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].roles :
            #print("SL-DEF printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].lines, "| role :", h.type, "| mainVar :", h.mainVar)
            if(h.type == "varDefine" and h.mainVar == criterionVariable) :
                #print("SL-DEF printing --> ", "here")
                return i
    return False

def finderSliceLoop(targetList = [], listOfEveryPentads = None, sn_idB = 0):
    """Takes the id of a statement and try to find a begLoop before this statement.
    If a begLoop is found, then search for the endLoop, then search for the loopCond,
    then return the three of them"""
    print("\nSL-LOO printing --> ", "Searchin loop for statement :", sn_idB)
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
                print("SL-LOO printing --> ", "begLoop found at statement :", begLoopStatement)
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
                    print("SL-LOO printing --> ", "endLoop found at statement :", endLoopStatement)
        i = 0
        for i in range (begLoopStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
            for h in listOfEveryPentads[i].roles :
                if(h.type == "loopCondition" and loopCondStatement == -1) :
                    listOfEveryPentads[i].useful = True
                    loopCondStatement = i
                    print("SL-LOO printing --> ", "and here is the loop condition :", loopCondStatement)
                    # then add other variables to target list I guess...
    return [begLoopStatement, endLoopStatement, loopCondStatement]
        


