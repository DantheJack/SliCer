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
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].role :
            #print("SL-DEC printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].line, "| role :", h.type, "| mainVar :", h.mainVar)
            if(h.type == "varDeclar" and h.mainVar == criterionVariable) :
                #print("SL-DEC printing --> ", "here")
                listOfEveryPentads[i].useful = True
                return True
    return False            
    
def finderSliceDefine(listOfEveryPentads = None, criterionVariable = "a", criterionStatement = None):
    for i in range (criterionStatement, -1, -1): #decremental for loop so we need to read number 0 (that's why we count -1 until we reach -1)
        for h in listOfEveryPentads[i].role :
            print("SL-DEF printing --> ", "st :", i, "| lines :", listOfEveryPentads[i].line, "| role :", h.type, "| mainVar :", h.mainVar)
            if(h.type == "varDefine" and h.mainVar == criterionVariable) :
                print("SL-DEF printing --> ", "here")
                listOfEveryPentads[i].useful = True
                return True