from pentadClass import pentadStruct, printAll, printAllWithRoles
from LexicalAnalyser import mainLexicalAnalyser
from SyntacticAnalyser import mainSyntacticAnalyser
from SemanticAnalyser import mainSemanticalAnalyser
import os
import string
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
#import platform    
#print(platform.python_implementation()) --> CPython
#cls & pytest -rA -s -v

########################################################################################################
def mainCompleteAnalyser(sourceCodeScrolledText = None, resultTextArea=None, criterionVariable = 'a', criterionLine = 20, eraser = False):

    file = open('src/sourceCode.txt','w')
    file.write(sourceCodeScrolledText.get("1.0", tk.END))
    file.close()
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./src/sourceCode.txt"
    #targetFileCompletePath = "./testfiles/testfileSlice13.c"
    print()
    debugMode = False
    result = mainLexicalAnalyser(targetFileCompletePath, debugMode)
    pentadList = result[0]
    if pentadList == []:
        if(debugMode) :
            print("\n\n\t\tNo code left to analyse, unfortunately... Please, try with another code.\n") ###############################################
            print("\n\t\tIf the problem persists, you are invited to report it in GitHub --> SliCer --> Issues.") #####################################
            print("\n\t\tIt would be a rather easy way to participate to the development of this project. Thanks.\n\n") ###############################
        if(not debugMode) :
            messagebox.showerror(title="Something's wrong, I can feel it...", message=\
 "It seems that there is a problem with your code. Please, try something else.\
\n\nIf the problem persists, you are invited to report it in GitHub --> SliCer --> Issues.\
 It would be an easy way to participate to the development of this project.\
\n\nDemo_version : You can also send me an email directly at dan.lipskier@hotmail.fr")
        
    targetFileAllTextLines = result[1]
    #for line in targetFileAllTextLines:           ###### A ENLEVER
    #    sourceCodeScrolledText.insert(END, line)  ###### A ENLEVER

    print()
    pentadList = mainSyntacticAnalyser(pentadList, debugMode)
    print()
    pentadList = mainSemanticalAnalyser(pentadList, criterionVariable, criterionLine, debugMode)
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
    resultTextArea.delete('0.0', tk.END)

#  #  #  #
    if(eraser == False):
        for line in targetFileAllTextLines:
            x += 1
            utility = 0
            for o in range (len(pentadList)):
                
                if (pentadList[o].useful and pentadList[o].lines[0] <= x and x <= pentadList[o].lines[1]):
                    utility = 1
            if (utility == 1):
                print(" --> " + "[ " + str(x) + " ]\t" + line)
                resultTextArea.insert(tk.END, line, 'in') 
            else :
                print("     " + "[ " + str(x) + " ]\t" + line)
                resultTextArea.insert(tk.END, line, 'out') 
        print()
#  #  #  #
    if(eraser == True):
        for line in targetFileAllTextLines:
            x += 1
            utility = 0
            for o in range (len(pentadList)):
                
                if (pentadList[o].useful and pentadList[o].lines[0] <= x and x <= pentadList[o].lines[1]):
                    utility = 1
            if (utility == 1):
                print(" oo> " + "[ " + str(x) + " ]\t" + line)
                resultTextArea.insert(tk.END, line) 
            else :
                print("     " + "[ " + str(x) + " ]\t" + line)
                resultTextArea.insert(tk.END, "\n") 
        print()
#  #  #  #

    #print("**************Affichage des roles*****************")

    #for o in pentadList:
    #   for p in o.roles:
    #      #print(str(o.lines) , ".   " , o.text , " ---> " , p.type, " : ", p.var)
    ############
    ############


