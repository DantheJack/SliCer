from pentadClass import pentadStruct
from LexicalAnalyser import spaceNormalizer
import re

def findS1(listOfEveryPentads = None, criterionLine = 9):
    S1 = 0
    i = 0
    for i in range (len(listOfEveryPentads)):
#        print("0.2 printing --> ", "st ", listOfEveryPentads[i].id, ": ", listOfEveryPentads[i].text, " \t---\t ", listOfEveryPentads[i].line[1], " - ", listOfEveryPentads[i].line[0])      
        if(listOfEveryPentads[i].line[0] <= criterionLine):
            S1 = i
    return S1


def finderSliceDeclar(listOfEveryPentads = None, criterionVariable = "a", criterionStatement = None):
    sn_idA = 0
    i = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].role :
            #print("SL-DEC printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].line, "| role :", h.type, "| mainVar :", h.mainVar)
            if(h.type == "varDeclar" and h.mainVar == criterionVariable) :
                #print("SL-DEC printing --> ", "here")
                listOfEveryPentads[i].useful = True
                return True
    return False
    
def finderSliceDefine(listOfEveryPentads = None, criterionVariable = "a", criterionStatement = None):
    sn_idB = 0
    i = 0
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].role :
            #print("SL-DEF printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].line, "| role :", h.type, "| mainVar :", h.mainVar)
            if(h.type == "varDefine" and h.mainVar == criterionVariable) :
                #print("SL-DEF printing --> ", "here")
                listOfEveryPentads[i].useful = True
                sn_idB = i
                return sn_idB
    

def finderSliceLoop(targetList = [], listOfEveryPentads = None, sn_idB = 0):
    print("SL-LOO printing --> ", "called w/ statement :", sn_idB)
    i = 0
    loopCount = 1
    begLoopStatement = -1
    endLoopStatement = -1
    Sn_idC = -1
    for i in range (sn_idB, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].role :
            if(h.type == "loopBeg") : loopCount = loopCount - 1
            if(h.type == "loopEnd") : loopCount = loopCount + 1
            if(loopCount == 0 and begLoopStatement == -1) :
                listOfEveryPentads[i].useful = True
                begLoopStatement = i
                print("SL-LOO printing --> ", "begLoop found at statement :", begLoopStatement)
    if(begLoopStatement == -1):
        return
    else :
        i = 0
        loopCount = 1
        for i in range (begLoopStatement + 1, len(listOfEveryPentads)): #incremental for loop to find the endLoop
            for h in listOfEveryPentads[i].role :
                if(h.type == "loopBeg") : loopCount = loopCount + 1
                if(h.type == "loopEnd") : loopCount = loopCount - 1
                if(loopCount == 0 and endLoopStatement == -1) :
                    listOfEveryPentads[i].useful = True
                    endLoopStatement = i
                    print("SL-LOO printing --> ", "begLoop found at statement :", endLoopStatement)
        i = 0
        for i in range (begLoopStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
            for h in listOfEveryPentads[i].role :
                if(h.type == "loopCondition" and Sn_idC == -1) :
                    listOfEveryPentads[i].useful = True
                    Sn_idC = i
                    print("SL-LOO printing --> ", "and here is the loop condition :", endLoopStatement)
                    # then add other variables to target list I guess...

        finderSliceLoop(listOfEveryPentads, Sn_idC)


