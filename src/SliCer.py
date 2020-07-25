from CompleteAnalyser import mainCompleteAnalyser
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os

#print(os.path.basename(os.getcwd()))
while ((os.path.basename(os.getcwd())) != "src") :
    os.chdir(os.path.dirname(os.getcwd()))
    #print(" - ")

#print("src =", os.path.basename(os.getcwd()))

mainWindow = tk.Tk()
mainWindow['bg']='light blue'
mainWindow.geometry("1090x800")
mainWindow.title("SliCer")
mainWindow.resizable(False, False)
############
############
########################################################################################################
mainFrame = tk.Frame(master=mainWindow, bd=4, width=1090, height=800, padx=5, pady=5)
mainFrame.grid(row=0,column=0, sticky='nesw')
mainFrame.grid_propagate(0)
mainFrame['bg']='black'
########################################################################################################
#
########################################################################################################
leftFrame = tk.LabelFrame(master=mainFrame, bd=4, width=540, height=685, text="Source code", fg='white', padx=20, pady=20)
leftFrame.grid(row=2,column=0, sticky='nesw')
leftFrame.grid_propagate(0)
leftFrame['bg']='dark blue'

##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

sourceCodeTextContainer = tk.Frame(leftFrame, borderwidth=0, relief="sunken")

var = tk.StringVar()
label = tk.Label(sourceCodeTextContainer, textvariable=var, fg="white", bg="dark blue", font=('Courrier New', '10'))
var.set("1. \n2. \n3. \n4. \n5. \n6. \n8. \n9. \n10. \n11. \n12. \n13. \n14. \n15. \n16. \n17. \n18. \n19. \n20. \n21. \n22. \n23. \n24. \n25. \n26. \n27. \n28. \n29. \n30. \n31. \n32. \n33. \n34. \n35. \n36. \n. \n. \n. \n ")
label.grid(row=0, column=0, sticky="news", rowspan= 2)

sourceCodeScrolledText = tk.Text(sourceCodeTextContainer, width=61, height=34, wrap="none", borderwidth=0, font=('Courrier', '10'), undo = True, spacing1 = 0.13) ################# # # #
sourceCodeTextVsb = tk.Scrollbar(sourceCodeTextContainer, orient="vertical", command=sourceCodeScrolledText.yview)
sourceCodeTextHsb = tk.Scrollbar(sourceCodeTextContainer, orient="horizontal", command=sourceCodeScrolledText.xview)
sourceCodeScrolledText.configure(yscrollcommand=sourceCodeTextVsb.set, xscrollcommand=sourceCodeTextHsb.set)

sourceCodeScrolledText.grid(row=0, column=1, sticky="nsew")
sourceCodeTextVsb.grid(row=0, column=2, sticky="ns")
sourceCodeTextHsb.grid(row=1, column=1, sticky="ew")

sourceCodeTextContainer.grid_rowconfigure(0, weight=1)
sourceCodeTextContainer.grid_columnconfigure(0, weight=1)

sourceCodeTextContainer.pack(side="top", fill="both", expand=True)


sourceCodeScrolledText.insert(tk.END, "\nCopy/Paste or type your source code here.") 

sourceCodeScrolledText.insert(tk.END, "\n\n\n\nWarning : If your C code contains syntax error, \
\nthe slicing will result in errors or inaccuracies.") 

sourceCodeScrolledText.insert(tk.END, "\n\n\n\n\nIn this version, you are invited to use \
\nvariable definitions, comments, strings, variables declarations, \
\nincrement and decrement operators, while loops, do-while loops, \
\nfor loops, affectation operator and escaped newlines.") 
sourceCodeScrolledText.insert(tk.END, "\n\nHowever, pleace notice that IF/ELSE statements \
\nand Defines / Macros are not implemented yet.") 
sourceCodeScrolledText.insert(tk.END, "\n\n\nI still do believe that this demo version offers \
\na satisfaying demonstration of the solution and its capabilities.\n") 

##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
########################################################################################################
#
########################################################################################################
middleFrame = tk.Frame(master=mainFrame, bd=4, width=10, height=685)
middleFrame.grid(row=2,column=1, sticky='nesw')
middleFrame.grid_propagate(0)
middleFrame['bg']='dark blue'
########################################################################################################
#
########################################################################################################
rightFrame = tk.LabelFrame(master=mainFrame, bd=4, width=540, height=685, text="Result slice", fg='white', padx=20, pady=20)
rightFrame.grid(row=2,column=2, sticky='nesw')
rightFrame.grid_propagate(0)
rightFrame['bg']='dark blue'
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

resultTextContainer = tk.Frame(rightFrame, borderwidth=0, relief="sunken")
resultTextContainer.grid(column = 1, sticky = 'w')
var = tk.StringVar()
label = tk.Label(resultTextContainer, textvariable=var, fg="white", bg="dark blue", font=('Courrier New', '10'))
var.set("1. \n2. \n3. \n4. \n5. \n6. \n8. \n9. \n10. \n11. \n12. \n13. \n14. \n15. \n16. \n17. \n18. \n19. \n20. \n21. \n22. \n23. \n24. \n25. \n26. \n27. \n28. \n29. \n30. \n31. \n32. \n33. \n34. \n35. \n36. \n. \n. \n. \n ")
label.grid(row=0, column=0, sticky="news", rowspan= 2)
resultScrolledText = tk.Text(resultTextContainer, width=62, height=34, wrap="none", borderwidth=0, font=('Courrier', '10'), undo = True, spacing1 = 0.13)       ################# # # #
resultTextVsb = tk.Scrollbar(resultTextContainer, orient="vertical", command=resultScrolledText.yview)
resultTextHsb = tk.Scrollbar(resultTextContainer, orient="horizontal", command=resultScrolledText.xview)
resultScrolledText.configure(yscrollcommand=resultTextVsb.set, xscrollcommand=resultTextHsb.set)

resultScrolledText.grid(row=0, column=1, sticky="nsew")
resultTextVsb.grid(row=0, column=2, sticky="ns")
resultTextHsb.grid(row=1, column=1, sticky="ew")

resultTextContainer.grid_rowconfigure(0, weight=1)
resultTextContainer.grid_columnconfigure(0, weight=1)

resultTextContainer.pack(side="top", fill="both", expand=True)

resultScrolledText.tag_config('in', foreground='red')
resultScrolledText.tag_config('out', foreground='black')

##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
########################################################################################################
#
########################################################################################################
upFrame = tk.Frame(master=mainFrame, bd=4, width=1070, height=90, padx=10)
upFrame['bg']='dark blue'
upFrame.grid(row=0, columnspan =3,column=0, sticky='nesw')
upFrame.grid_propagate(0)
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
firstUpFrame = tk.Frame(master=upFrame, bd=4, width=170, height=120, padx=10, pady=10)
firstUpFrame['bg']='dark blue'
firstUpFrame.grid(row=0, columnspan =1,column=0, sticky='nw')
firstUpFrame.grid_propagate(0)
secondUpFrame = tk.Frame(master=upFrame, bd=4, width=170, height=120, padx=5, pady=10)
secondUpFrame['bg']='dark blue'
secondUpFrame.grid(row=0, columnspan =1,column=1, sticky='nw')
secondUpFrame.grid_propagate(0)
thirdUpFrame = tk.Frame(master=upFrame, bd=4, width=280, height=120, padx=5, pady=10)
thirdUpFrame['bg']='dark blue'
thirdUpFrame.grid(row=0, columnspan =1,column=2, sticky='nsw')
thirdUpFrame.grid_propagate(0)
fourthUpFrame = tk.Frame(master=upFrame, bd=4, width=100, height=120, padx=5, pady=10)
fourthUpFrame['bg']='dark blue'
fourthUpFrame.grid(row=0, columnspan =1,column=3, sticky='nsw')
fourthUpFrame.grid_propagate(0)
                                                
labelCriterionVar = tk.Label(thirdUpFrame, text="Slicing Criterion Variable  ", anchor="e")
labelCriterionVar.grid(row=0, column=0, pady=1)
labelCriterionVar['bg']='dark blue'
labelCriterionVar['fg']='white'
entryCriterionVar = tk.Entry(thirdUpFrame, bd=1, width=18)
entryCriterionVar.grid(row=0, column=1, pady=1, sticky='w')
entryCriterionVar['bg']='white'
entryCriterionVar['fg']='black'
entryCriterionVar['exportselection']=0

labelCriterionLine = tk.Label(thirdUpFrame, text="    Slicing Criterion Line  ", anchor="e")
labelCriterionLine.grid(row=1, column=0, pady=1)
labelCriterionLine['bg']='dark blue'
labelCriterionLine['fg']='white'
entryCriterionLine = tk.Entry(thirdUpFrame, bd=1, width=4)
entryCriterionLine.grid(row=1, column=1, pady=1, sticky='w')
entryCriterionLine['bg']='white'
entryCriterionLine['fg']='black'
entryCriterionLine['exportselection']=0

#fullLinesCheckValue = tk.BooleanVar() 
#fullLinesCheckButton = tk.Checkbutton(secondUpFrame, text = "  Check to highlight FULL LINES of the original code, \
#\n  even if only part of the line is relevant to the slice. \
#\n  Warning : The final slice could be unexecutable.", 
#                  variable = fullLinesCheckValue, justify=tk.LEFT, onvalue = True, offvalue = False)
#fullLinesCheckButton['bg']='white'
#fullLinesCheckButton['fg']='black'
#fullLinesCheckButton.pack()
eraserCheckValue = tk.BooleanVar() 
eraserCheckValue.set(True)
eraserCheckButton = tk.Checkbutton(firstUpFrame, text = "  Check to display the entire original code with lines containing elements \
\n  of the slice in RED font and the rest in BLACK font. \
\n  If unchecked, only elements that are part of the final slice will be displayed.",  
                  variable = eraserCheckValue, justify=tk.LEFT, onvalue = True, offvalue = False)
eraserCheckButton['bg']='white'
eraserCheckButton['fg']='black'
eraserCheckButton.pack()

########################################################################################################
#
buttonSlice = tk.Button(fourthUpFrame, text =" Slice ", padx=3, pady=3, font=('Arial', '12', 'bold'), \
                        command = lambda: mainCompleteAnalyser(sourceCodeScrolledText, resultScrolledText, \
                            eraser = eraserCheckValue.get(), \
                            criterionVariable = entryCriterionVar.get(), criterionLine = int(entryCriterionLine.get())))
buttonSlice.grid(sticky='nesw')

mainWindow.mainloop()