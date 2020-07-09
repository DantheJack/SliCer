from pentadClass import pentadStruct, printAll, printAllWithRoles, printAllLoopCondVariables, printAllVarDefVariables
from LexicalAnalyser import *
from SyntacticAnalyser import *
import os
import string
#import platform    
#print(platform.python_implementation()) --> CPython
#cls & pytest -rA -s -v


print("MAIN printing --> ", "******** PRE-PROCESSING **********")
print("MAIN printing --> ", "*********** readlines ************")
os.chdir(os.getcwd())                                       #####
targetFile = open("./testfiles/ULTIMATE/testfileULTIMATE.c", "r") ###################################
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
print("MAIN printing --> ", "********** PSEUDO-LEXING ************")
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

#print("MAIN printing --> ", "***************** PSEUDO-PARSING *********************")



#for o in targetFileListOfPentads:
    #print(str(o.line) + ".   " + o.text)

#print("**************Affichage des roles*****************")

#for o in targetFileListOfPentads:
 #   for p in o.role:
 #      #print(str(o.line) , ".   " , o.text , " ---> " , p.type, " : ", p.var)
