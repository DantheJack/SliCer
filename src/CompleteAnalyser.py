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

localDebug = False
debugMode = False

########################################################################################################
def mainCompleteAnalyser(sourceCodeScrolledText = None, resultTextArea=None, criterionVariable = None, criterionLine = 10000, eraser = False):
    if(not criterionVariable): return False
    file = open('sourceCode.txt','w')
    if(not localDebug):
        file.write(sourceCodeScrolledText.get("1.0", tk.END))     #for test purposes, comment this
    file.close()
    os.chdir(os.getcwd())                                       
    if(not localDebug):
        targetFileCompletePath = "./sourceCode.txt"               #for test purposes, comment this
    if(localDebug):
        targetFileCompletePath = "./testfiles/testfileSliceUrgent.c"   #for test purposes, UNcomment this
        criterionVariable = "mean"
        criterionLine = 80
    print()

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
    if(not localDebug):
        resultTextArea.delete('0.0', tk.END)     #for test purposes, comment this

#  #  #  #
    if(eraser == True):
        for line in targetFileAllTextLines:
            utility = 0
            for o in range (len(pentadList)):
                if (pentadList[o].useful and pentadList[o].lines[0] <= x and x <= pentadList[o].lines[1]):
                    utility = 1
            if (utility == 1):
                print(" --> " + "[ " + str(x) + " ]\t" + line)
                if(not localDebug):
                    resultTextArea.insert(tk.END, line, 'in') #for test purposes, comment this
            else :
                print("     " + "[ " + str(x) + " ]\t" + line)
                if(not localDebug):
                    resultTextArea.insert(tk.END, line, 'out') #for test purposes, comment this
            x += 1
        print()
#  #  #  #
    if(eraser == False):
        for line in targetFileAllTextLines:
            utility = 0
            for o in range (len(pentadList)):
                if (pentadList[o].useful and pentadList[o].lines[0] <= x and x <= pentadList[o].lines[1]):
                    utility = 1
            if (utility == 1):
                print(" ~~> " + "[ " + str(x) + " ]\t" + line)
                if(not localDebug):
                    resultTextArea.insert(tk.END, line)     #for test purposes, comment this
            else :
                print("     " + "[ " + str(x) + " ]\t" + line)
                if(not localDebug):
                    resultTextArea.insert(tk.END, "\n")     #for test purposes, comment this
            x += 1
        print()
#  #  #  #

    #print("**************Affichage des roles*****************")

    #for o in pentadList:
    #   for p in o.roles:
    #      #print(str(o.lines) , ".   " , o.text , " ---> " , p.type, " : ", p.var)
    ############
    ############

if(localDebug): mainCompleteAnalyser(criterionVariable = "end", criterionLine = 10000)     #for test purposes, UNcomment this