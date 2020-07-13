from globalVariables import PENTADprinter

class pentadStruct:
    """Class representing a line of the subject, containing :
    - its number
    - its full text
    - its list of roles & variables
    - its significance"""

    def __init__(self, line, text): # Notre méthode constructeur
        self.id = 0
        if (len(line) != 2):
            line.append(line[0])
        self.line = line
        self.text = text
        self.role = [roleStruct()]
        self.useful = False
        if(self.text != "" and PENTADprinter):
            print("PENTAD printing --> ", "New Pentad created : (", self.line, ", \"" + str(self.text) + "\" )")

    def addRole(self, roleName, mainVar = None, otherVars = []):
        if(self.role[0].type == "unknown"):
            del self.role[:]
        self.role.append(roleStruct(roleName, mainVar, otherVars))
        print("PENTAD printing --> ", "Role added : ", roleName, " for ", mainVar) if PENTADprinter and roleName != "unknown" else False
        if(mainVar): return roleName + " of " + mainVar
        else: return roleName

    def printing(self):
        if self.line[0] == self.line[1] :
            return str("  [  " + str(self.line[0]) + "  ]" + "  \t—   " + self.text)
        else :
            return str("  " + str(self.line) + "  \t—   " + self.text) 
            
    def searchForRole(self, roleToSearch):
        for role in self.role:
            if role.type == roleToSearch : return True
        return False



class roleStruct:
    """Class representing a role fulfilled by a line of the subject, containing :
    - its type (defVar, initVar, beginIf, etc...)
    - its variable (if one is needed)
    """
    def __init__(self, type = "unknown", mainVar = None, otherVars = []): # Notre méthode constructeur
        self.type = type
        self.mainVar = mainVar
        self.otherVars = otherVars


def printAll(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:

        #print(o.printing() + space + o.role[0].type)
        print(o.printing())
    print("")

def printAllWithRoles2(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:
        space = ""
        length = 80-len(o.printing())
        if(o.line[0] == o.line[1] and o.line[0] < 10): length = length - 1
        if(o.line[0] != o.line[1] and o.line[0] < 10): length = length - 1
        if(o.line[0] != o.line[1] and o.line[1] < 10): length = length - 1
        for char in range (length):
            space += " "
        if (len(o.role) > 1):
            if(not o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type)
            if(o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" + ", " + o.role[1].type)
            if(not o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type + " (" + o.role[1].mainVar + ")")
            if(o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" ", " + o.role[1].type + " (" + o.role[1].mainVar + ")")
        else :
            if(o.role[0].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")")
            else:
                print(o.printing() + space + o.role[0].type)
    print("")

def printAllWithRoles(listOfEveryPentads = None):
    print("")
    max_size = 0
    for o in listOfEveryPentads:
        if(len(o.printing()) > max_size) :
            max_size = len(o.printing())
    for o in listOfEveryPentads:
        space = ""
        length = max_size + 5 -len(o.printing())
        if(o.line[0] == o.line[1] and o.line[0] < 10): length = length - 1
        if(o.line[0] != o.line[1] and o.line[0] < 10): length = length - 1
        if(o.line[0] != o.line[1] and o.line[1] < 10): length = length - 1
        for char in range (length):
            space += " "
        if (len(o.role) >= 3):
            if(not o.role[2].mainVar and not o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type + ", " + o.role[2].type)
            if(not o.role[2].mainVar and o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" + ", " + o.role[1].type + ", " + o.role[2].type)
            if(not o.role[2].mainVar and not o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type + " (" + o.role[1].mainVar + ")" + ", " + o.role[2].type)
            if(not o.role[2].mainVar and o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" ", " + o.role[1].type + " (" + o.role[1].mainVar + ")" + ", " + o.role[2].type)
            if(o.role[2].mainVar and not o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type + ", " + o.role[2].type + " (" + o.role[2].mainVar + ")")
            if(o.role[2].mainVar and o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" + ", " + o.role[1].type + ", " + o.role[2].type + " (" + o.role[2].mainVar + ")")
            if(o.role[2].mainVar and not o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type + " (" + o.role[1].mainVar + ")" ", " + o.role[2].type + " (" + o.role[2].mainVar + ")")
            if(o.role[2].mainVar and o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" ", " + o.role[1].type + " (" + o.role[1].mainVar + ")" ", " + o.role[2].type + " (" + o.role[2].mainVar + ")")
        
        if (len(o.role) == 2):
            if(not o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type)
            if(o.role[0].mainVar and not o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" + ", " + o.role[1].type)
            if(not o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + ", " + o.role[1].type + " (" + o.role[1].mainVar + ")")
            if(o.role[0].mainVar and o.role[1].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")" ", " + o.role[1].type + " (" + o.role[1].mainVar + ")")
        if (len(o.role) == 1):
            if(o.role[0].mainVar):
                print(o.printing() + space + o.role[0].type + " (" + o.role[0].mainVar + ")")
            else:
                print(o.printing() + space + o.role[0].type)
    print("")

def printAllLoopCondVariables(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:
        if (len(o.role) > 1):
            if(o.role[0].type == "loopCondition"):
                print(o.printing() + " --- LoopCondition :")
                for otherVar in o.role[0].otherVars :
                    print(" --> " + otherVar )
                print("")
            elif(o.role[1].type == "loopCondition"):
                print(o.printing() + " --- LoopCondition :")
                for otherVar in o.role[1].otherVars :
                    print(" --> " + otherVar )
                print("")
        else :
            if(o.role[0].type == "loopCondition"):
                print(o.printing() + " --- LoopCondition :")
                for otherVar in o.role[0].otherVars :
                    print(" --> " + otherVar )
                print("")

    print("")

def printAllVarDefVariables(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:
        for role in o.role:
            if(role.type == "varDefine"):
                print(o.printing() + " --- varDefine of " + role.mainVar)
                print("")
                for otherVar in role.otherVars :
                    print(" \t\t\t--> " + otherVar )
                    print("")

    print("")