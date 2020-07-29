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
        self.lines = line
        self.text = text
        self.roles = [roleStruct()]
        self.useful = False
        if(self.text != "" and PENTADprinter):
            print("PENTAD printing --> ", "New Pentad created : (", self.lines, ", \"" + str(self.text) + "\" )")

    def addRole(self, roleName, mainVar = None, otherVars = []):
        if(self.roles[0].type == "unknown"):
            del self.roles[:]
        cancelAdding = False
        for h in self.roles :
            if(h.type == roleName and h.mainVar == mainVar and h.otherVars == otherVars):
                cancelAdding = True
        if(cancelAdding) :
            print("PENTAD printing --> ", "Role : ", roleName, " for ", mainVar, "was already given to this statement.") if PENTADprinter and roleName != "unknown" else False
        else :
            self.roles.append(roleStruct(roleName, mainVar, otherVars))
            print("PENTAD printing --> ", "Role added : ", roleName, " for ", mainVar) if PENTADprinter and roleName != "unknown" else False
        if(mainVar): return roleName + " of " + mainVar
        else: return roleName

    def printing(self):
        if self.lines[0] == self.lines[1] :
            return str("[  " + str(self.lines[0]) + "  ]" + "  \t—   " + self.text)
        else :
            return str(str(self.lines) + "  \t—   " + self.text) 
            
    def searchForRole(self, roleToSearch):
        for role in self.roles:
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

        #print(o.printing() + space + o.roles[0].type)
        print(o.printing())
    print("")

def printAllWithRoles2(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:
        space = ""
        length = 80-len(o.printing())
        if(o.lines[0] == o.lines[1] and o.lines[0] < 10): length = length - 1
        if(o.lines[0] != o.lines[1] and o.lines[0] < 10): length = length - 1
        if(o.lines[0] != o.lines[1] and o.lines[1] < 10): length = length - 1
        for char in range (length):
            space += " "
        if (len(o.roles) > 1):
            if(not o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type)
            if(o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" + ", " + o.roles[1].type)
            if(not o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")")
            if(o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")")
        else :
            if(o.roles[0].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")")
            else:
                print(o.printing() + space + o.roles[0].type)
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
        if(o.lines[0] == o.lines[1] and o.lines[0] < 10): length = length - 1
        if(o.lines[0] != o.lines[1] and o.lines[0] < 10): length = length - 1
        if(o.lines[0] != o.lines[1] and o.lines[1] < 10): length = length - 1
        for char in range (length):
            space += " "
        if (len(o.roles) >= 3):
            if(not o.roles[2].mainVar and not o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type + ", " + o.roles[2].type)
            if(not o.roles[2].mainVar and o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" + ", " + o.roles[1].type + ", " + o.roles[2].type)
            if(not o.roles[2].mainVar and not o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")" + ", " + o.roles[2].type)
            if(not o.roles[2].mainVar and o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")" + ", " + o.roles[2].type)
            if(o.roles[2].mainVar and not o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type + ", " + o.roles[2].type + " (" + o.roles[2].mainVar + ")")
            if(o.roles[2].mainVar and o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" + ", " + o.roles[1].type + ", " + o.roles[2].type + " (" + o.roles[2].mainVar + ")")
            if(o.roles[2].mainVar and not o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")" ", " + o.roles[2].type + " (" + o.roles[2].mainVar + ")")
            if(o.roles[2].mainVar and o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")" ", " + o.roles[2].type + " (" + o.roles[2].mainVar + ")")
        
        if (len(o.roles) == 2):
            if(not o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type)
            if(o.roles[0].mainVar and not o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" + ", " + o.roles[1].type)
            if(not o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")")
            if(o.roles[0].mainVar and o.roles[1].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")" ", " + o.roles[1].type + " (" + o.roles[1].mainVar + ")")
        if (len(o.roles) == 1):
            if(o.roles[0].mainVar):
                print(o.printing() + space + o.roles[0].type + " (" + o.roles[0].mainVar + ")")
            else:
                print(o.printing() + space + o.roles[0].type)
    print("")

def printAllLoopCondVariables(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:
        if (len(o.roles) > 1):
            if(o.roles[0].type == "loopCondition"):
                print(o.printing() + " --- LoopCondition :")
                for otherVar in o.roles[0].otherVars :
                    print(" --> " + otherVar )
                print("")
            elif(o.roles[1].type == "loopCondition"):
                print(o.printing() + " --- LoopCondition :")
                for otherVar in o.roles[1].otherVars :
                    print(" --> " + otherVar )
                print("")
        else :
            if(o.roles[0].type == "loopCondition"):
                print(o.printing() + " --- LoopCondition :")
                for otherVar in o.roles[0].otherVars :
                    print(" --> " + otherVar )
                print("")
    print("")

def printAllIfCondVariables(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:
        if (len(o.roles) > 1):
            if(o.roles[0].type == "ifCondition"):
                print(o.printing() + " --- IfCondition :")
                for otherVar in o.roles[0].otherVars :
                    print(" --> " + otherVar )
                print("")
            elif(o.roles[1].type == "ifCondition"):
                print(o.printing() + " --- IfCondition :")
                for otherVar in o.roles[1].otherVars :
                    print(" --> " + otherVar )
                print("")
        else :
            if(o.roles[0].type == "ifCondition"):
                print(o.printing() + " --- IfCondition :")
                for otherVar in o.roles[0].otherVars :
                    print(" --> " + otherVar )
                print("")
    print("")

def printAllVarDefVariables(listOfEveryPentads = None):
    print("")
    for o in listOfEveryPentads:
        for role in o.roles:
            if(role.type == "varDefine"):
                print(o.printing() + " --- varDefine of " + role.mainVar)
                print("")
                for otherVar in role.otherVars :
                    print(" \t\t\t--> " + otherVar )
                    print("")

    print("")