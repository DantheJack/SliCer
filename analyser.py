from pentadClass import pentadStruct, printAll, printAllWithRoles, printAllLoopCondVariables, printAllVarDefVariables
from LexicalAnalyser import *
from SyntacticAnalyser import *
from SemanticAnalyser import *
import os
import string
#import platform    
#print(platform.python_implementation()) --> CPython
#cls & pytest -rA -s -v

print()
print("———————————————————————————— LEXICAL ANALYSIS ———————————————————————————")
print()
print("MAIN printing --> ", "*********** readlines ************")
os.chdir(os.getcwd())                                       #####
targetFile = open("./testfiles/testfileSlice4.c", "r") ###################################
targetFileLines = targetFile.readlines()                    #####
targetFile.close()
targetFileListOfPentads = []
targetFileListOfPentads.append(pentadStruct([0], "")) # just to start at targetFileListOfPentads[1]
for i in range (len(targetFileLines)):
    newPentad = pentadStruct([i], targetFileLines[i])
    targetFileListOfPentads.append(newPentad)
targetFileListOfPentads.append(pentadStruct([0], "//")) # because stringReducer and maybe some others have troubles dealing with
print("MAIN printing --> ", "********* spaceNormalizer ********")   # the very last Pentad of the list
#targetFileListOfPentads = spaceNormalizer(spaceNormalizer(targetFileListOfPentads))
#printAll(targetFileListOfPentads)
print("MAIN printing --> ", "********* commentsEraser *********")
targetFileListOfPentads = commentsEraser(targetFileListOfPentads)
printAll(targetFileListOfPentads)
print("MAIN printing --> ", "********* stringReducer **********")
targetFileListOfPentads = stringReducer(targetFileListOfPentads)
printAll(targetFileListOfPentads)
print("MAIN printing --> ", "******** doWhileConverter ********")
targetFileListOfPentads = doWhileConverter(targetFileListOfPentads)
printAllWithRoles(targetFileListOfPentads)
print("MAIN printing --> ", "******** whileLoopConverter ********")
targetFileListOfPentads = whileLoopConverter(targetFileListOfPentads)
printAllWithRoles(targetFileListOfPentads)
print("MAIN printing --> ", "******* semicolonBasedChopper *******")
targetFileListOfPentads = semicolonBasedChopper(targetFileListOfPentads)
printAllWithRoles(targetFileListOfPentads)
print("MAIN printing --> ", "********** multiLineManager *********")
targetFileListOfPentads = multiLineManager(targetFileListOfPentads)
printAllWithRoles(targetFileListOfPentads)
print()
print("——————————————————————————— SYNTACTIF ANALYSIS ——————————————————————————")
print()
print("MAIN printing --> ", "****** forLoopRoleAssignment *******")
targetFileListOfPentads = forLoopRoleAssignment(targetFileListOfPentads)
printAllWithRoles(targetFileListOfPentads)
#printAllLoopCondVariables(targetFileListOfPentads)
print("MAIN printing --> ", "********** varDecDetector **********")
targetFileListOfPentads = varDecDetector(targetFileListOfPentads)
printAllWithRoles(targetFileListOfPentads)
print("MAIN printing --> ", "********** varDefDetector **********")
targetFileListOfPentads = varDefDetector(targetFileListOfPentads)
printAllWithRoles(targetFileListOfPentads)
#printAllVarDefVariables(targetFileListOfPentads)
print()
print("——————————————————————————— SEMANTICAL ANALYSIS —————————————————————————")
print()
fullLines = True

for o in range (len(targetFileListOfPentads)):
    targetFileListOfPentads[o].id = o           #id of a PENTAD = order in the list
print()
for o in range (len(targetFileListOfPentads)):
    if targetFileListOfPentads[o].useful :
        print(o, ".\t", "--> " + str(targetFileListOfPentads[o].lines) + ".   " + targetFileListOfPentads[o].text)
    else :
        print(o, ".\t", "    " + str(targetFileListOfPentads[o].lines) + ".   " + targetFileListOfPentads[o].text)
print()

criterionVariable = 'a'
criterionLine = 20
criterionStatement = findS1(targetFileListOfPentads, criterionLine)
targetList = [[criterionVariable, criterionStatement]]
i = 0
while i < len(targetList):
    print("\nWe progress through targetList (i =", i, ", len =", len(targetList), ")")
    print("\ncouple = [var =", targetList[i][0], ", st =", targetList[i][1], "]")
    idOfDeclaration = finderSliceDeclar(targetFileListOfPentads, targetList[i][0], targetList[i][1]-1)
    targetFileListOfPentads[idOfDeclaration].useful = True
    idOfDefinition = finderSliceDefine(targetFileListOfPentads, targetList[i][0], targetList[i][1]-1)
    for role in targetFileListOfPentads[idOfDefinition].roles:
        if(role.type == "varDefine"):
            for othervariable in role.otherVars :
                targetList += [[othervariable, idOfDefinition]]
                print("\nAdded : ", othervariable, " to targetList w/ st ", idOfDefinition)
    targetFileListOfPentads[idOfDefinition].useful = True
    isThisStatementInALoop = idOfDefinition
    begLoopStatement = -2
    endLoopStatement = -2
    loopCondStatement = -2
    while(begLoopStatement != -1 and endLoopStatement != -1 and loopCondStatement != -1):
        result = finderSliceLoop(targetList, targetFileListOfPentads, isThisStatementInALoop)
        begLoopStatement = result[0]
        endLoopStatement = result[1]
        loopCondStatement = result[2]
        if(begLoopStatement != -1):
            targetFileListOfPentads[begLoopStatement].useful = True
        if(endLoopStatement != -1):
            targetFileListOfPentads[endLoopStatement].useful = True
        if(loopCondStatement != -1):
            targetFileListOfPentads[loopCondStatement].useful = True
            for role in targetFileListOfPentads[loopCondStatement].roles:
                if(role.type == "loopCondition"):
                    for othervariable in role.otherVars :
                        targetList += [[othervariable, loopCondStatement]]
                        print("\nAdded : ", othervariable, " to targetList w/ st ", loopCondStatement)
        isThisStatementInALoop = loopCondStatement

    i += 1




print()
print("—————————————————————————————————————————————————————————————————————————")
print("———————————————————————————————— RESULTS ————————————————————————————————")
print("—————————————————————————————————————————————————————————————————————————")
print()
for o in range (len(targetFileListOfPentads)):
    if targetFileListOfPentads[o].useful :
        print(o, ".\t", "--> " + str(targetFileListOfPentads[o].lines) + ".   " + targetFileListOfPentads[o].text)
    else :
        print(o, ".\t", "    " + str(targetFileListOfPentads[o].lines) + ".   " + targetFileListOfPentads[o].text)
print()
print("—————————————————————————————————————————————————————————————————————————")
print()
x = 0
for line in targetFileLines:
    x += 1
    utility = 0
    for o in range (len(targetFileListOfPentads)):
        if (targetFileListOfPentads[o].useful and targetFileListOfPentads[o].lines[0] <= x and x <= targetFileListOfPentads[o].lines[1]):
            utility = 1
    if (utility == 1):
        print(" --> " + "[ " + str(x) + " ]\t" + line)
    else :
        print("     " + "[ " + str(x) + " ]\t" + line)


#print("**************Affichage des roles*****************")

#for o in targetFileListOfPentads:
 #   for p in o.roles:
 #      #print(str(o.lines) , ".   " , o.text , " ---> " , p.type, " : ", p.var)
