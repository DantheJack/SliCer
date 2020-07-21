from pentadClass import pentadStruct, printAll, printAllWithRoles
from LexicalAnalyser import mainLexicalAnalyser
from SyntacticAnalyser import mainSyntacticAnalyser
from SemanticAnalyser import mainSemanticalAnalyser
import os
import string
#import platform    
#print(platform.python_implementation()) --> CPython
#cls & pytest -rA -s -v

os.chdir(os.getcwd())                                       
targetFileCompletePath = "./testfiles/testfileSlice8.c"
criterionVariable = 'a'
criterionLine = 20
print()
result = mainLexicalAnalyser(targetFileCompletePath, True)
pentadList = result[0]
targetFileAllTextLines = result[1]
print()
pentadList = mainSyntacticAnalyser(pentadList, True)
print()
pentadList = mainSemanticalAnalyser(pentadList, criterionVariable, criterionLine, True)
print()
print("—————————————————————————————————————————————————————————————————————————")
print("———————————————————————————————— RESULTS ————————————————————————————————")
print("—————————————————————————————————————————————————————————————————————————")
print()
for pentadNumber in range (len(pentadList)):
    if pentadList[pentadNumber].useful :
        print(pentadList[pentadNumber].id, ".\t", "--> " + str(pentadList[pentadNumber].lines) + ".   " + pentadList[pentadNumber].text)
    else :
        print(pentadList[pentadNumber].id, ".\t", "    " + str(pentadList[pentadNumber].lines) + ".   " + pentadList[pentadNumber].text)
print()
print("—————————————————————————————————————————————————————————————————————————")
print()
x = 0
for line in targetFileAllTextLines:
    x += 1
    utility = 0
    for o in range (len(pentadList)):
        if (pentadList[o].useful and pentadList[o].lines[0] <= x and x <= pentadList[o].lines[1]):
            utility = 1
    if (utility == 1):
        print(" --> " + "[ " + str(x) + " ]\t" + line)
    else :
        print("     " + "[ " + str(x) + " ]\t" + line)

print()

#print("**************Affichage des roles*****************")

#for o in pentadList:
 #   for p in o.roles:
 #      #print(str(o.lines) , ".   " , o.text , " ---> " , p.type, " : ", p.var)
