import os
import pytest
from pentadClass import pentadStruct
from LexicalAnalyser import spaceNormalizer, commentsEraser, stringReducer, multiLineManager, semicolonBasedChopper, doWhileConverter, whileLoopConverter
#from CompleteAnalyser import mainCompleteAnalyser
from LexicalAnalyser import mainLexicalAnalyser
from SyntacticAnalyser import mainSyntacticAnalyser
from SemanticAnalyser import mainSemanticalAnalyser

def test_spaceNormalizer():
    os.chdir(os.getcwd())  
    myTemporaryTestFile = open("./testfiles/testfileSpaces.c", "r")
    testFileLines = myTemporaryTestFile.readlines()
    myTemporaryTestFile.close()
    testFileListOfPentads = []
    testFileListOfPentads.append(pentadStruct([0], "")) # just to start at testFileListOfPentads[1]

    for i in range (len(testFileLines)):
        testFileListOfPentads.append(pentadStruct([i+1], testFileLines[i]))

    testFileListOfPentads = spaceNormalizer(testFileListOfPentads)
    #print("---")
    #for i in range (len(testFileListOfPentads)):
        #print(testFileListOfPentads[i].text)
    #print("---")
    assert testFileListOfPentads[1].text == "1"
    assert testFileListOfPentads[2].text == "2"
    assert testFileListOfPentads[3].text == "3"
    assert testFileListOfPentads[4].text == "4"
    assert testFileListOfPentads[5].text == "5"
    assert testFileListOfPentads[6].text == "6"
    assert testFileListOfPentads[7].text == "7"
    assert testFileListOfPentads[8].text == "8 9"
    assert testFileListOfPentads[9].text == "10 11"
    assert testFileListOfPentads[10].text == "12 13 14"
    assert testFileListOfPentads[11].text == "15 16 17"
    assert testFileListOfPentads[12].text == "\"18\""
    assert testFileListOfPentads[13].text == "\" 19\""
    assert testFileListOfPentads[14].text == "\"20 \""
    assert testFileListOfPentads[15].text == "\" 21 \""
    assert testFileListOfPentads[16].text == "\"  22\""
    assert testFileListOfPentads[17].text == "\"  23 \""
    assert testFileListOfPentads[18].text == "\"  24  \""
    assert testFileListOfPentads[19].text == "\" 25  \""
    assert testFileListOfPentads[20].text == "\" 26  \" 27"
    assert testFileListOfPentads[21].text == "\"  28 29  \" 30"
    assert testFileListOfPentads[22].text == "\" 31\" 32 33"
    assert testFileListOfPentads[23].text == "\" 34  35\" 36 37"
    assert testFileListOfPentads[24].text == "\"  38  \" 39 \"40\" 41"
    assert testFileListOfPentads[25].text == "\" 42  \" 43 44\"  45  46  \" 47"
    assert testFileListOfPentads[26].text == "\"  48"
    assert testFileListOfPentads[27].text == "\""
    assert testFileListOfPentads[28].text == "\"  49  "
    assert testFileListOfPentads[29].text == "  \""
    assert testFileListOfPentads[30].text == "\" 50"
    assert testFileListOfPentads[31].text == "51  "
    assert testFileListOfPentads[32].text == "\""
    assert testFileListOfPentads[33].text == "\" "
    assert testFileListOfPentads[34].text == "  52"
    assert testFileListOfPentads[35].text == "  53\""
    assert testFileListOfPentads[36].text == "54\"\"55"
    assert testFileListOfPentads[37].text == "56 \"\" 57"
    assert testFileListOfPentads[38].text == "\"\"\"58"
    assert testFileListOfPentads[39].text == "  59\"\"\" 60"
    assert testFileListOfPentads[40].text == "61 \"\" 62 63\"" 
    assert testFileListOfPentads[41].text == "64  \"65 66\" "
    assert testFileListOfPentads[42].text == "\"67\"  68  "

def test_commentsEraser():
    os.chdir(os.getcwd())
    myTemporaryTestFile = open("./testfiles/testfileComments.c", "r")
    testFileLines = myTemporaryTestFile.readlines()
    myTemporaryTestFile.close()
    testFileListOfPentads = []
    testFileListOfPentads.append(pentadStruct([0], "not relevant;")) # just to start at testFileListOfPentads[1]
    #print("Added : " + testFileListOfPentads[0].text)
    for i in range (len(testFileLines)):
        testFileListOfPentads.append(pentadStruct([i+1], testFileLines[i]))
        #print("Added : " + testFileListOfPentads[i+1].text)
    #print("Text = ")
    #print(spaceNormalizer(testFileListOfPentads[0].text))
    #print("Size = ")
    #print(len(spaceNormalizer(testFileListOfPentads[0].text)))
    testFileListOfPentads = commentsEraser(testFileListOfPentads)
    testFileListOfPentads = spaceNormalizer(testFileListOfPentads)
    #print("---")
    #for i in range (len(testFileListOfPentads)):
        #print(testFileListOfPentads[i].text)
    #print("---")
    assert testFileListOfPentads[1].text == "/0/"
    assert testFileListOfPentads[2].text == ""
    assert testFileListOfPentads[3].text == ""
    assert testFileListOfPentads[4].text == ""
    assert testFileListOfPentads[5].text == ""
    assert testFileListOfPentads[6].text == ""
    assert testFileListOfPentads[7].text == ""
    assert testFileListOfPentads[8].text == "/ /8"
    assert testFileListOfPentads[9].text == "/"
    assert testFileListOfPentads[10].text == ""
    assert testFileListOfPentads[11].text == ""
    assert testFileListOfPentads[12].text == ""
    assert testFileListOfPentads[13].text == ""
    assert testFileListOfPentads[14].text == ""
    assert testFileListOfPentads[15].text == ""
    assert testFileListOfPentads[16].text == ""
    assert testFileListOfPentads[17].text == ""
    assert testFileListOfPentads[18].text == ""
    assert testFileListOfPentads[19].text == ""
    assert testFileListOfPentads[20].text == ""
    assert testFileListOfPentads[21].text == ""
    assert testFileListOfPentads[22].text == "1718"
    assert testFileListOfPentads[23].text == ""
    assert testFileListOfPentads[24].text == "/20*"
    assert testFileListOfPentads[25].text == ""
    assert testFileListOfPentads[26].text == "24"
    assert testFileListOfPentads[27].text == ""
    assert testFileListOfPentads[28].text == "*/26"
    assert testFileListOfPentads[29].text == "/27*/28"
    assert testFileListOfPentads[30].text == "30"
    assert testFileListOfPentads[31].text == ""
    assert testFileListOfPentads[32].text == "**3335"
    assert testFileListOfPentads[33].text == ""
    assert testFileListOfPentads[34].text == "*/37"
    assert testFileListOfPentads[35].text == "38*"
    assert testFileListOfPentads[36].text == "/39"
    assert testFileListOfPentads[37].text == "\"/*41*/\""
    assert testFileListOfPentads[38].text == "\"//42\""
    assert testFileListOfPentads[39].text == "\"43*///44\"45"
    assert testFileListOfPentads[40].text == ""
    assert testFileListOfPentads[41].text == ""
    assert testFileListOfPentads[42].text == ""
    assert testFileListOfPentads[43].text == "49\"/* 50 */\"51"
    assert testFileListOfPentads[44].text == "\"//\"52"
    assert testFileListOfPentads[45].text == "\"/*\"53\"*/\""
    assert testFileListOfPentads[46].text == ""
    assert testFileListOfPentads[47].text == "\"55*/\"56*/57"
    assert testFileListOfPentads[48].text == "\" 58//\"/\"/\"*59"
    assert testFileListOfPentads[49].text == "60*/"
    assert testFileListOfPentads[50].text == "\"//*61*/*\""
    assert testFileListOfPentads[51].text == ""
    assert testFileListOfPentads[52].text == ""
    assert testFileListOfPentads[53].text == "64"
    assert testFileListOfPentads[54].text == "67\"//68\""
    assert testFileListOfPentads[55].text == "\"70//"
    assert testFileListOfPentads[56].text == "72\"\"\"71"
    assert testFileListOfPentads[57].text == "73\"*/"
    assert testFileListOfPentads[58].text == "75\""
    assert testFileListOfPentads[59].text == "76\"\\\"77?//\\\\78;\";"
    assert testFileListOfPentads[60].text == "79\"//80"
    assert testFileListOfPentads[61].text == "\\\"/*81\"82\"\\"
    assert testFileListOfPentads[62].text == "83*/ 84  //\"\\"
    assert testFileListOfPentads[63].text == "87*/88\"89\"\\\"90/*"
    assert testFileListOfPentads[64].text == "91\""


def test_stringReducer():
    os.chdir(os.getcwd())
    myTemporaryTestFile = open("./testfiles/testfileStrings.c", "r")
    testFileLines = myTemporaryTestFile.readlines()
    myTemporaryTestFile.close()
    testFileListOfPentads = []
    testFileListOfPentads.append(pentadStruct([0], "not relevant;")) # just to start at testFileListOfPentads[1]

    for i in range (len(testFileLines)):
        testFileListOfPentads.append(pentadStruct([i+1], testFileLines[i]))

    testFileListOfPentads = stringReducer(testFileListOfPentads)
    #print("---")
    #for i in range (len(testFileListOfPentads)):
    #   #print(testFileListOfPentads[i].text)
    #print("---")
    assert testFileListOfPentads[1].text == "1"
    assert testFileListOfPentads[2].text == "\"\""
    assert testFileListOfPentads[3].text == "3 \"\""
    assert testFileListOfPentads[4].text == "\"\" 7"
    assert testFileListOfPentads[5].text == "\"\" 10"
    assert testFileListOfPentads[6].text == "11\"\"13\"\"14\""
    assert testFileListOfPentads[7].text == "\"\"\"17"
    assert testFileListOfPentads[8].text == "18\""
    assert testFileListOfPentads[9].text == "\"22\'\"\"\\\"\"23"
    assert testFileListOfPentads[10].text == "24\""
    assert testFileListOfPentads[11].text == ""
    assert testFileListOfPentads[12].text == "\""
    assert testFileListOfPentads[13].text == "25\"\"\""
    assert testFileListOfPentads[14].text == ""
    assert testFileListOfPentads[15].text == "\"28"
    assert testFileListOfPentads[16].text == "\"\""
    assert testFileListOfPentads[17].text == "30 = \"\";"


def test_doWhileConverter():
    #assuming stringReducer and spaceNormalizer work nicely
    os.chdir(os.getcwd())
    myTemporaryTestFile = open("./testfiles/testfileDoWhiles.c", "r")
    testFileLines = myTemporaryTestFile.readlines()
    myTemporaryTestFile.close()
    testFileListOfPentads = []
    testFileListOfPentads.append(pentadStruct([0], "not relevant;")) # just to start at testFileListOfPentads[1]
    for i in range (len(testFileLines)):
        testFileListOfPentads.append(pentadStruct([i+1], testFileLines[i]))

    testFileListOfPentads = doWhileConverter(stringReducer(spaceNormalizer(testFileListOfPentads)))
    #print("---")
    #for i in range (len(testFileListOfPentads)):
       #print(testFileListOfPentads[i].text)
    #print("---")
    assert testFileListOfPentads[1].text == "for( x > 1 )"
    assert testFileListOfPentads[1].lines == [1, 1]
    assert testFileListOfPentads[2].text == "{"
    assert testFileListOfPentads[2].lines == [2, 2]
    assert testFileListOfPentads[3].text == "y = f( x );not"
    assert testFileListOfPentads[4].text == ";"
    assert testFileListOfPentads[5].text == "x--;"
    assert testFileListOfPentads[6].text == "}"
    assert testFileListOfPentads[6].lines == [6, 6]
    assert testFileListOfPentads[6].roles[0].type == "while of do from line"
    assert testFileListOfPentads[6].roles[0].mainVar == str(1)
    assert testFileListOfPentads[7].text == ""
    assert testFileListOfPentads[8].text == "int stupid=\"\";for (i=2; i <3.4 ; i++){"
    assert testFileListOfPentads[8].lines == [8, 8]
    assert testFileListOfPentads[9].text == "dosomething;"
    assert testFileListOfPentads[10].text == "formidable; }"
    assert testFileListOfPentads[11].text == ""
    assert testFileListOfPentads[12].text == "int compteur = 5;"
    assert testFileListOfPentads[13].text == ""
    assert testFileListOfPentads[14].text == "for(6; 7>8.9;10++){"
    assert testFileListOfPentads[15].text == "for(11){;}"
    assert testFileListOfPentads[15].lines == [15, 15]
    assert testFileListOfPentads[15].roles[0].type == "while of do from line"
    assert testFileListOfPentads[15].roles[0].mainVar == str(15)
    assert testFileListOfPentads[16].text == "}"
    assert testFileListOfPentads[17].text == "(12)"
    assert testFileListOfPentads[18].text == "(13)while(14){15}"
    assert testFileListOfPentads[19].text == "//"
    assert testFileListOfPentads[20].text == "for(nothinggood != !True || compteur< 19){"
    assert testFileListOfPentads[20].lines == [20, 20]
    assert testFileListOfPentads[21].text == "for(formidable === ++i++) \\"
    assert testFileListOfPentads[21].lines == [21, 21]
    assert testFileListOfPentads[22].text == "{ \\"
    assert testFileListOfPentads[22].lines == [22, 22]
    assert testFileListOfPentads[23].text == "compteur ++;for(dosomething!=17+18){nothinggood; 16;\\"
    assert testFileListOfPentads[23].lines == [23, 23]
    assert testFileListOfPentads[24].text == "}}"
    assert testFileListOfPentads[24].lines == [24, 24]
    assert testFileListOfPentads[24].roles[0].type == "while of do from line"
    assert testFileListOfPentads[24].roles[0].mainVar == str(21)
    assert testFileListOfPentads[24].roles[1].type == "while of do from line"
    assert testFileListOfPentads[24].roles[1].mainVar == str(23)
    assert testFileListOfPentads[25].text == ""
    assert testFileListOfPentads[25].lines == [25, 25]
    assert testFileListOfPentads[26].text == "}"
    assert testFileListOfPentads[26].lines == [26, 26]
    assert testFileListOfPentads[26].roles[0].type == "while of do from line"
    assert testFileListOfPentads[26].roles[0].mainVar == str(20)
    assert testFileListOfPentads[27].text == ""
    assert testFileListOfPentads[28].text == "for(smthg)\\"
    assert testFileListOfPentads[29].text == "{"
    assert testFileListOfPentads[30].text == "for(2){;}(31)int a32 =\\"
    assert testFileListOfPentads[31].text == "33\\"
    assert testFileListOfPentads[32].text == ";}"
    assert testFileListOfPentads[33].text == "for(34){;}"



def test_WhileLoopConverter():
    os.chdir(os.getcwd())
    myTemporaryTestFile = open("./testfiles/testfileWhiles.c", "r")
    testFileLines = myTemporaryTestFile.readlines()
    myTemporaryTestFile.close()
    testFileListOfPentads = []
    testFileListOfPentads.append(pentadStruct([0], "not relevant;")) # just to start at testFileListOfPentads[1]
    for i in range (len(testFileLines)):
        testFileListOfPentads.append(pentadStruct([i+1], testFileLines[i]))

    testFileListOfPentads = whileLoopConverter(spaceNormalizer(testFileListOfPentads))
    #print("---")
    #for i in range (len(testFileListOfPentads)):
       #print(testFileListOfPentads[i].text)
    #print("---")
    assert testFileListOfPentads[1].text == "long char awhile = '1', whi = '2', le;"
    assert testFileListOfPentads[2].text == "int whiled=1;"
    assert testFileListOfPentads[3].text == "2;for(whiled <= 3)"
    assert testFileListOfPentads[4].text == "{"
    assert testFileListOfPentads[5].text == "printf(\"3%d \", whiled);"
    assert testFileListOfPentads[6].text == "count++;"
    assert testFileListOfPentads[7].text == "} for(whi > le){"
    assert testFileListOfPentads[8].text == "printf(\"%s\",whi);le;"
    assert testFileListOfPentads[9].text == "m--;} for(whiled){for(whiled == whi+le)"
    assert testFileListOfPentads[10].text == "{"
    assert testFileListOfPentads[11].text == "}}"
    assert testFileListOfPentads[12].text == "for(i<=10){ j=1; for(j<=10){ printf(\"*\"); j++; } printf(\"something\"); i++;for(True)"
    assert testFileListOfPentads[13].text == "{}"
    assert testFileListOfPentads[14].text == "}"



def test_MultiLineManager():
    #assuming semiColonBasedChopper, doWhileConverter and spaceNormalizer work nicely
    #it should be since they are all tested before test_SpaceSemiMultiManager.
    os.chdir(os.getcwd())
    myTemporaryTestFile = open("./testfiles/testfileMultiLines.c", "r")
    testFileLines = myTemporaryTestFile.readlines()
    myTemporaryTestFile.close()
    testFileListOfPentads = []
    testFileListOfPentads.append(pentadStruct([0], "not relevant;")) # just to start at testFileListOfPentads[1]
    for i in range (len(testFileLines)):
        testFileListOfPentads.append(pentadStruct([i+1], testFileLines[i]))

    testFileListOfPentads = multiLineManager(semicolonBasedChopper(doWhileConverter(spaceNormalizer(testFileListOfPentads))))
    #print("---")
    #for i in range (len(testFileListOfPentads)):
       #print(testFileListOfPentads[i].text)
    #print("---")
    assert testFileListOfPentads[1].text == "1;"
    assert testFileListOfPentads[1].lines == [1, 1]
    assert testFileListOfPentads[2].text == "2 ;"
    assert testFileListOfPentads[2].lines == [2, 2]
    assert testFileListOfPentads[3].text == "3 ;"
    assert testFileListOfPentads[3].lines == [3, 3]
    assert testFileListOfPentads[4].text == "4 ;"
    assert testFileListOfPentads[4].lines == [3, 3]
    assert testFileListOfPentads[5].text == "5 6;"
    assert testFileListOfPentads[5].lines == [4, 5]
    assert testFileListOfPentads[6].text == "7;"
    assert testFileListOfPentads[6].lines == [6, 6]
    assert testFileListOfPentads[7].text == "8 9;"
    assert testFileListOfPentads[7].lines == [6, 8]
    assert testFileListOfPentads[8].text == "10, 11;"
    assert testFileListOfPentads[8].lines == [9, 9]
    assert testFileListOfPentads[9].text == "12 13 14 15 ;"
    assert testFileListOfPentads[9].lines == [9, 13]
    assert testFileListOfPentads[10].text == "16;"
    assert testFileListOfPentads[10].lines == [13, 13]
    assert testFileListOfPentads[11].text == "17 ;"
    assert testFileListOfPentads[11].lines == [14, 15]
    assert testFileListOfPentads[12].text == ";"
    assert testFileListOfPentads[12].lines == [15, 15]
    assert testFileListOfPentads[13].text == "18"
    assert testFileListOfPentads[13].lines == [15, 15]
    assert testFileListOfPentads[14].text == "{"
    assert testFileListOfPentads[14].lines == [15, 15]
    assert testFileListOfPentads[15].text == "19;"
    assert testFileListOfPentads[15].lines == [16, 16]
    assert testFileListOfPentads[16].text == "20 ;"
    assert testFileListOfPentads[16].lines == [17, 18]
    assert testFileListOfPentads[17].text == ";"
    assert testFileListOfPentads[17].lines == [19, 19]
    assert testFileListOfPentads[18].text == "21"
    assert testFileListOfPentads[18].lines == [19, 19]
    assert testFileListOfPentads[19].text == "}"
    assert testFileListOfPentads[19].lines == [19, 19]
    assert testFileListOfPentads[20].text == "22;"
    assert testFileListOfPentads[20].lines == [20, 20]
    assert testFileListOfPentads[21].text == "\"\"23;"
    assert testFileListOfPentads[21].lines == [20, 20]
    assert testFileListOfPentads[22].text == "24 \"\" 25;"
    assert testFileListOfPentads[22].lines == [20, 22]
    assert testFileListOfPentads[23].text == "for (26; 27<28.29;30++)"
    assert testFileListOfPentads[23].lines == [23, 23]
    assert testFileListOfPentads[24].text == "{"
    assert testFileListOfPentads[24].lines == [24, 24]
    assert testFileListOfPentads[25].text == "for (2)"
    assert testFileListOfPentads[25].lines == [25, 25]
    assert testFileListOfPentads[26].text == "{"
    assert testFileListOfPentads[26].lines == [25, 25]
    assert testFileListOfPentads[27].text == ";"
    assert testFileListOfPentads[27].lines == [25, 25]
    assert testFileListOfPentads[28].text == "}"
    assert testFileListOfPentads[28].lines == [25, 25]
    assert testFileListOfPentads[28].roles[0].type == "while of do from line"
    assert testFileListOfPentads[28].roles[0].mainVar == str(25)
    assert testFileListOfPentads[29].text == "(31)int a32 = 33 ;"
    assert testFileListOfPentads[29].lines == [25, 27]
    assert testFileListOfPentads[30].text == "}"
    assert testFileListOfPentads[30].roles[0].type == "unknown"
    assert testFileListOfPentads[30].lines == [27, 27]
    assert testFileListOfPentads[31].text == "float for1 = 2;"
    assert testFileListOfPentads[31].lines == [31, 31]
    assert testFileListOfPentads[32].text == "signed char unsignedint=\"\";"
    assert testFileListOfPentads[32].lines == [32, 32]

#multiLineManager does not really handle multiline for, while or do-while loops.
#It does handle conditions () and executions statement {} ... probably.

def test_slice1():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice1.c"
    criterionVariable = 'a'
    criterionLine = 9
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == True
    assert testFileListOfPentads[1].useful == True
    assert testFileListOfPentads[2].useful == True
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == True
    assert testFileListOfPentads[6].useful == True
    assert testFileListOfPentads[7].useful == True
    assert testFileListOfPentads[8].useful == True
    assert testFileListOfPentads[9].useful == True
    assert testFileListOfPentads[10].useful == True
    assert testFileListOfPentads[11].useful == True
    assert testFileListOfPentads[12].useful == False

def test_slice2():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice2.c"
    criterionVariable = 'a'
    criterionLine = 9
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == True
    assert testFileListOfPentads[1].useful == True
    assert testFileListOfPentads[2].useful == True
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == False
    assert testFileListOfPentads[6].useful == False
    assert testFileListOfPentads[7].useful == False
    assert testFileListOfPentads[8].useful == False
    assert testFileListOfPentads[9].useful == True
    assert testFileListOfPentads[10].useful == True
    assert testFileListOfPentads[11].useful == True
    assert testFileListOfPentads[12].useful == False

def test_slice3():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice3.c"
    criterionVariable = 'a'
    criterionLine = 9
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == True
    assert testFileListOfPentads[1].useful == True
    assert testFileListOfPentads[2].useful == True
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == True
    assert testFileListOfPentads[6].useful == True
    assert testFileListOfPentads[7].useful == True
    assert testFileListOfPentads[8].useful == True
    assert testFileListOfPentads[9].useful == True
    assert testFileListOfPentads[10].useful == True
    assert testFileListOfPentads[11].useful == True
    assert testFileListOfPentads[12].useful == False

def test_slice4():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice4.c"
    criterionVariable = 'a'
    criterionLine = 9
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == True
    assert testFileListOfPentads[1].useful == True
    assert testFileListOfPentads[2].useful == True
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == True
    assert testFileListOfPentads[6].useful == False
    assert testFileListOfPentads[7].useful == False
    assert testFileListOfPentads[8].useful == False
    assert testFileListOfPentads[9].useful == False
    assert testFileListOfPentads[10].useful == True
    assert testFileListOfPentads[11].useful == True
    assert testFileListOfPentads[12].useful == False


def test_slice5():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice5.c"
    criterionVariable = 'a'
    criterionLine = 14
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == True
    assert testFileListOfPentads[1].useful == True
    assert testFileListOfPentads[2].useful == True
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == True
    assert testFileListOfPentads[6].useful == True
    assert testFileListOfPentads[7].useful == True
    assert testFileListOfPentads[8].useful == True
    assert testFileListOfPentads[9].useful == True
    assert testFileListOfPentads[10].useful == True
    assert testFileListOfPentads[11].useful == True
    assert testFileListOfPentads[12].useful == True
    assert testFileListOfPentads[13].useful == True
    assert testFileListOfPentads[14].useful == True
    assert testFileListOfPentads[15].useful == True
    assert testFileListOfPentads[16].useful == True
    assert testFileListOfPentads[17].useful == True
    assert testFileListOfPentads[18].useful == True
    assert testFileListOfPentads[19].useful == True
    assert testFileListOfPentads[20].useful == True
    assert testFileListOfPentads[21].useful == True
    assert testFileListOfPentads[22].useful == False

def test_slice6():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice6.c"
    criterionVariable = 'a'
    criterionLine = 20
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == True
    assert testFileListOfPentads[1].useful == True
    assert testFileListOfPentads[2].useful == False
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == False
    assert testFileListOfPentads[6].useful == True
    assert testFileListOfPentads[7].useful == False
    assert testFileListOfPentads[8].useful == True
    assert testFileListOfPentads[9].useful == True
    assert testFileListOfPentads[10].useful == True
    assert testFileListOfPentads[11].useful == True
    assert testFileListOfPentads[12].useful == True
    assert testFileListOfPentads[13].useful == False
    assert testFileListOfPentads[14].useful == True
    assert testFileListOfPentads[15].useful == True
    assert testFileListOfPentads[16].useful == True
    assert testFileListOfPentads[17].useful == True
    assert testFileListOfPentads[18].useful == True
    assert testFileListOfPentads[19].useful == True
    assert testFileListOfPentads[20].useful == True
    assert testFileListOfPentads[21].useful == True
    assert testFileListOfPentads[22].useful == True
    assert testFileListOfPentads[23].useful == True
    assert testFileListOfPentads[24].useful == True
    assert testFileListOfPentads[25].useful == True
    assert testFileListOfPentads[26].useful == False
    assert testFileListOfPentads[27].useful == False
    assert testFileListOfPentads[28].useful == True
    assert testFileListOfPentads[29].useful == False

def test_slice7():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice7.c"
    criterionVariable = 'a'
    criterionLine = 20
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == True
    assert testFileListOfPentads[1].useful == True
    assert testFileListOfPentads[2].useful == True
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == False
    assert testFileListOfPentads[6].useful == True
    assert testFileListOfPentads[7].useful == True
    assert testFileListOfPentads[8].useful == False
    assert testFileListOfPentads[9].useful == False
    assert testFileListOfPentads[10].useful == False
    assert testFileListOfPentads[11].useful == False
    assert testFileListOfPentads[12].useful == True
    assert testFileListOfPentads[13].useful == False
    assert testFileListOfPentads[14].useful == True
    assert testFileListOfPentads[15].useful == False
    assert testFileListOfPentads[16].useful == True
    assert testFileListOfPentads[17].useful == True
    assert testFileListOfPentads[18].useful == True
    assert testFileListOfPentads[19].useful == False
    assert testFileListOfPentads[20].useful == False
    assert testFileListOfPentads[21].useful == False
    assert testFileListOfPentads[22].useful == False
    assert testFileListOfPentads[23].useful == False
    assert testFileListOfPentads[24].useful == True
    assert testFileListOfPentads[25].useful == True
    assert testFileListOfPentads[26].useful == False
    assert testFileListOfPentads[27].useful == False
    assert testFileListOfPentads[28].useful == True
    assert testFileListOfPentads[29].useful == False

def test_slice8():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice8.c" #empty file
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mainLexicalAnalyser(targetFileCompletePath, True)
    assert pytest_wrapped_e.type == SystemExit

    #result = mainLexicalAnalyser(targetFileCompletePath)
    #testFileListOfPentads = result[0]
    #testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    #testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)


def test_slice9():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileSlice9.c" #file that became empty (comments)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mainLexicalAnalyser(targetFileCompletePath, True)
    assert pytest_wrapped_e.type == SystemExit
    
def test_scanf():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileScanf.c"
    criterionVariable = 'end'
    criterionLine = 100
    result = mainLexicalAnalyser(targetFileCompletePath)
    testFileListOfPentads = result[0]
    testFileListOfPentads = mainSyntacticAnalyser(testFileListOfPentads)
    testFileListOfPentads = mainSemanticalAnalyser(testFileListOfPentads, criterionVariable, criterionLine)
    assert testFileListOfPentads[0].useful == False
    assert testFileListOfPentads[1].useful == False
    assert testFileListOfPentads[2].useful == True
    assert testFileListOfPentads[3].useful == True
    assert testFileListOfPentads[4].useful == True
    assert testFileListOfPentads[5].useful == True
    assert testFileListOfPentads[6].useful == True
    assert testFileListOfPentads[7].useful == False
    assert testFileListOfPentads[8].useful == False
    assert testFileListOfPentads[9].useful == False
    assert testFileListOfPentads[10].useful == False
    assert testFileListOfPentads[11].useful == False
    assert testFileListOfPentads[12].useful == False
    assert testFileListOfPentads[13].useful == False
    assert testFileListOfPentads[14].useful == False
    assert testFileListOfPentads[15].useful == True
    assert testFileListOfPentads[16].useful == False
    assert testFileListOfPentads[17].useful == True
    assert testFileListOfPentads[18].useful == False
    assert testFileListOfPentads[19].useful == True
    assert testFileListOfPentads[20].useful == False
    assert testFileListOfPentads[21].useful == False
    assert testFileListOfPentads[22].useful == True
    assert testFileListOfPentads[23].useful == False
    assert testFileListOfPentads[24].useful == True
    assert testFileListOfPentads[25].useful == False
    assert testFileListOfPentads[26].useful == True
    assert testFileListOfPentads[27].useful == False
    assert testFileListOfPentads[28].useful == True
    assert testFileListOfPentads[29].useful == False
    assert testFileListOfPentads[30].useful == True
    assert testFileListOfPentads[31].useful == False
    assert testFileListOfPentads[32].useful == False
    assert testFileListOfPentads[33].useful == False
    assert testFileListOfPentads[34].useful == False
    assert testFileListOfPentads[35].useful == False
    assert testFileListOfPentads[36].useful == False
    assert testFileListOfPentads[37].useful == False
    assert testFileListOfPentads[38].useful == False
    assert testFileListOfPentads[39].useful == True
    assert testFileListOfPentads[40].useful == False
    assert testFileListOfPentads[41].useful == False
    assert testFileListOfPentads[42].useful == True
    assert testFileListOfPentads[43].useful == False
    assert testFileListOfPentads[44].useful == False
    assert testFileListOfPentads[45].useful == False
    assert testFileListOfPentads[46].useful == True
    assert testFileListOfPentads[47].useful == False
    assert testFileListOfPentads[48].useful == True
    assert testFileListOfPentads[49].useful == True
    assert testFileListOfPentads[50].useful == False

def test_IfElse():
    os.chdir(os.getcwd())                                       
    targetFileCompletePath = "./testfiles/testfileIfElse.c"

    result = mainLexicalAnalyser(targetFileCompletePath, True)
    testFileListOfPentads = []
    testFileListOfPentads.append(pentadStruct([0], "not relevant;")) # just to start at testFileListOfPentads[1] 
    testFileListOfPentads += result[0] 
    assert testFileListOfPentads[1].text == "void main (void)"
    assert testFileListOfPentads[2].text == "{"
    assert testFileListOfPentads[3].text == "int a = 0;"
    assert testFileListOfPentads[4].text == "int b = 0;"
    assert testFileListOfPentads[5].text == "int c;"
    assert testFileListOfPentads[6].text == "if(a == 0)"
    assert testFileListOfPentads[7].text == "{"
    assert testFileListOfPentads[8].text == "a = 1;" 
    assert testFileListOfPentads[9].text == "}" 
    assert testFileListOfPentads[10].text == "if(a == 0)" 
    assert testFileListOfPentads[11].text == "{"  
    assert testFileListOfPentads[12].text == "a = 2;" 
    assert testFileListOfPentads[13].text == "}" 
    assert testFileListOfPentads[14].text == "if(a == 0)" 
    assert testFileListOfPentads[15].text == "{" 
    assert testFileListOfPentads[16].text == "a = 3;"
    assert testFileListOfPentads[17].text == "}" 
    assert testFileListOfPentads[18].text == "if(a == 0)" 
    assert testFileListOfPentads[19].text == "{" 
    assert testFileListOfPentads[20].text == "a = 4;"  
    assert testFileListOfPentads[21].text == "}" 
    assert testFileListOfPentads[22].text == "else" 
    assert testFileListOfPentads[23].text == "{" 
    assert testFileListOfPentads[24].text == "a = 5;" 
    assert testFileListOfPentads[25].text == "}" 
    assert testFileListOfPentads[26].text == "if(a == 0)" 
    assert testFileListOfPentads[27].text == "{" 
    assert testFileListOfPentads[28].text == "a = 6;" 
    assert testFileListOfPentads[29].text == "}" 
    assert testFileListOfPentads[30].text == "else"  
    assert testFileListOfPentads[31].text == "{" 
    assert testFileListOfPentads[32].text == "a = 7;" 
    assert testFileListOfPentads[33].text == "}" 
    assert testFileListOfPentads[34].text == "if(a == 0)" 
    assert testFileListOfPentads[35].text == "{" 
    assert testFileListOfPentads[36].text == "a = 8;" 
    assert testFileListOfPentads[37].text == "}" 
    assert testFileListOfPentads[38].text == "else" 
    assert testFileListOfPentads[39].text == "{" 
    assert testFileListOfPentads[40].text == "a = 9;"  
    assert testFileListOfPentads[41].text == "}" 
    assert testFileListOfPentads[42].text == "if(a == 0)" 
    assert testFileListOfPentads[43].text == "{" 
    assert testFileListOfPentads[44].text == "a = 10;" 
    assert testFileListOfPentads[45].text == "}" 
    assert testFileListOfPentads[46].text == "a = 11;" 
    assert testFileListOfPentads[47].text == "if(a == 0)" 
    assert testFileListOfPentads[48].text == "{" 
    assert testFileListOfPentads[49].text == "a = 12;" 
    assert testFileListOfPentads[50].text == "}"  
    assert testFileListOfPentads[51].text == "a = 13;" 
    assert testFileListOfPentads[52].text == "if(a == 0)" 
    assert testFileListOfPentads[53].text == "{" 
    assert testFileListOfPentads[54].text == "a = 14;" 
    assert testFileListOfPentads[55].text == "}" 
    assert testFileListOfPentads[56].text == "else" 
    assert testFileListOfPentads[57].text == "{" 
    assert testFileListOfPentads[58].text == "for (a = 0; a < 0; a++)" 
    assert testFileListOfPentads[59].text == "{" 
    assert testFileListOfPentads[60].text == "if(a != 0)"  
    assert testFileListOfPentads[61].text == "{" 
    assert testFileListOfPentads[62].text == "a = a + 15;" 
    assert testFileListOfPentads[63].text == "}" 
    assert testFileListOfPentads[64].text == "}" 
    assert testFileListOfPentads[65].text == "}" 
    assert testFileListOfPentads[66].text == "if(b == 0)" 
    assert testFileListOfPentads[67].text == "{" 
    assert testFileListOfPentads[68].text == "b = 1;" 
    assert testFileListOfPentads[69].text == "}" 
    assert testFileListOfPentads[70].text == "else"  
    assert testFileListOfPentads[71].text == "{" 
    assert testFileListOfPentads[72].text == "if(b == 2)" 
    assert testFileListOfPentads[73].text == "{" 
    assert testFileListOfPentads[74].text == "b = 3;" 
    assert testFileListOfPentads[75].text == "}" 
    assert testFileListOfPentads[76].text == "}" 
    assert testFileListOfPentads[77].text == "if(b == 4)" 
    assert testFileListOfPentads[78].text == "{" 
    assert testFileListOfPentads[79].text == "b = 5;" 
    assert testFileListOfPentads[80].text == "}"  
    assert testFileListOfPentads[81].text == "else" 
    assert testFileListOfPentads[82].text == "{" 
    assert testFileListOfPentads[83].text == "if(b == 6)" 
    assert testFileListOfPentads[84].text == "{" 
    assert testFileListOfPentads[85].text == "b = 7;" 
    assert testFileListOfPentads[86].text == "}" 
    assert testFileListOfPentads[87].text == "}" 
    assert testFileListOfPentads[88].text == "b = 8;" 
    assert testFileListOfPentads[89].text == "if(b == 9)" 
    assert testFileListOfPentads[90].text == "{"  
    assert testFileListOfPentads[91].text == "b = 10;" 
    assert testFileListOfPentads[92].text == "}" 
    assert testFileListOfPentads[93].text == "else" 
    assert testFileListOfPentads[94].text == "{" 
    assert testFileListOfPentads[95].text == "if (b == 11)" 
    assert testFileListOfPentads[96].text == "{" 
    assert testFileListOfPentads[97].text == "b = 12;" 
    assert testFileListOfPentads[98].text == "}" 
    assert testFileListOfPentads[99].text == "}" 
    assert testFileListOfPentads[100].text == "b = 13;"
    assert testFileListOfPentads[101].text == "if(b == 14)"
    assert testFileListOfPentads[102].text == "{"
    assert testFileListOfPentads[103].text == "b = 15;"
    assert testFileListOfPentads[104].text == "}"
    assert testFileListOfPentads[105].text == "else"
    assert testFileListOfPentads[106].text == "{"
    assert testFileListOfPentads[107].text == "if (b == 16)"
    assert testFileListOfPentads[108].text == "{"
    assert testFileListOfPentads[109].text == "b = 17;"
    assert testFileListOfPentads[110].text == "}"
    assert testFileListOfPentads[111].text == "else"
    assert testFileListOfPentads[112].text == "{" 
    assert testFileListOfPentads[113].text == "if (b == 18)"
    assert testFileListOfPentads[114].text == "{" 
    assert testFileListOfPentads[115].text == "b = 19;" 
    assert testFileListOfPentads[116].text == "}"
    assert testFileListOfPentads[117].text == "}" 
    assert testFileListOfPentads[118].text == "}"
    assert testFileListOfPentads[119].text == "if(b == 20)" 
    assert testFileListOfPentads[120].text == "{"
    assert testFileListOfPentads[121].text == "b = 21;" 
    assert testFileListOfPentads[122].text == "}"
    assert testFileListOfPentads[123].text == "else" 
    assert testFileListOfPentads[124].text == "{" 
    assert testFileListOfPentads[125].text == "if (b == 22)"
    assert testFileListOfPentads[126].text == "{" 
    assert testFileListOfPentads[127].text == "b = 23;" 
    assert testFileListOfPentads[128].text == "}"
    assert testFileListOfPentads[129].text == "else" 
    assert testFileListOfPentads[130].text == "{"  
    assert testFileListOfPentads[131].text == "if (b == 24)"
    assert testFileListOfPentads[132].text == "{"
    assert testFileListOfPentads[133].text == "b = 25;"
    assert testFileListOfPentads[134].text == "}" 
    assert testFileListOfPentads[135].text == "else"
    assert testFileListOfPentads[136].text == "{" 
    assert testFileListOfPentads[137].text == "if (b == 26)"
    assert testFileListOfPentads[138].text == "{" 
    assert testFileListOfPentads[139].text == "b = 27;"
    assert testFileListOfPentads[140].text == "b = 28;"
    assert testFileListOfPentads[141].text == "}"
    assert testFileListOfPentads[142].text == "else"
    assert testFileListOfPentads[143].text == "{"
    assert testFileListOfPentads[144].text == "if (b == 29)" 
    assert testFileListOfPentads[145].text == "{"
    assert testFileListOfPentads[146].text == "b = 30;"
    assert testFileListOfPentads[147].text == "}"
    assert testFileListOfPentads[148].text == "}"
    assert testFileListOfPentads[149].text == "}" 
    assert testFileListOfPentads[150].text == "}"  
    assert testFileListOfPentads[151].text == "}"  
    assert testFileListOfPentads[152].text == "b = 31;"  
    assert testFileListOfPentads[153].text == "if(b == 29)"
    assert testFileListOfPentads[154].text == "{"
    assert testFileListOfPentads[155].text == "b = 30;"
    assert testFileListOfPentads[156].text == "}"
    assert testFileListOfPentads[157].text == "else"
    assert testFileListOfPentads[158].text == "{"
    assert testFileListOfPentads[159].text == "if (b == 31)"
    assert testFileListOfPentads[160].text == "{"  
    assert testFileListOfPentads[161].text == "b = 32;"
    assert testFileListOfPentads[162].text == "if(b == 33)" 
    assert testFileListOfPentads[163].text == "{"
    assert testFileListOfPentads[164].text == "b = 34;"
    assert testFileListOfPentads[165].text == "}"
    assert testFileListOfPentads[166].text == "else"
    assert testFileListOfPentads[167].text == "{"
    assert testFileListOfPentads[168].text == "if (b == 35)" 
    assert testFileListOfPentads[169].text == "{"
    assert testFileListOfPentads[170].text == "if(b == 41)"  
    assert testFileListOfPentads[171].text == "{"
    assert testFileListOfPentads[172].text == "b = 42;" 
    assert testFileListOfPentads[173].text == "}"
    assert testFileListOfPentads[174].text == "else" 
    assert testFileListOfPentads[175].text == "{"
    assert testFileListOfPentads[176].text == "if(b == 43)"
    assert testFileListOfPentads[177].text == "{" 
    assert testFileListOfPentads[178].text == "b = 44;"
    assert testFileListOfPentads[179].text == "if(b == 45)"
    assert testFileListOfPentads[180].text == "{" 
    assert testFileListOfPentads[181].text == "b = 46;" 
    assert testFileListOfPentads[182].text == "}"
    assert testFileListOfPentads[183].text == "else" 
    assert testFileListOfPentads[184].text == "{"
    assert testFileListOfPentads[185].text == "if (b == 47)" 
    assert testFileListOfPentads[186].text == "{"
    assert testFileListOfPentads[187].text == "b = 48;"
    assert testFileListOfPentads[188].text == "}" 
    assert testFileListOfPentads[189].text == "}"
    assert testFileListOfPentads[190].text == "}" 
    assert testFileListOfPentads[191].text == "else"
    assert testFileListOfPentads[192].text == "{"
    assert testFileListOfPentads[193].text == "if(b == 49)"
    assert testFileListOfPentads[194].text == "{"
    assert testFileListOfPentads[195].text == "b = 50;" 
    assert testFileListOfPentads[196].text == "b = 51;"
    assert testFileListOfPentads[197].text == "}" 
    assert testFileListOfPentads[198].text == "else"
    assert testFileListOfPentads[199].text == "{"
    assert testFileListOfPentads[200].text == "b = 52;"
    assert testFileListOfPentads[201].text == "}"
    assert testFileListOfPentads[202].text == "}"
    assert testFileListOfPentads[203].text == "}"
    assert testFileListOfPentads[204].text == "if(b == 53)"
    assert testFileListOfPentads[205].text == "{"
    assert testFileListOfPentads[206].text == "b = 54;"
    assert testFileListOfPentads[207].text == "}"
    assert testFileListOfPentads[208].text == "else" 
    assert testFileListOfPentads[209].text == "{" 
    assert testFileListOfPentads[210].text == "b = 55;" 
    assert testFileListOfPentads[211].text == "}"  
    assert testFileListOfPentads[212].text == "b = 56;" 
    assert testFileListOfPentads[213].text == "}" 
    assert testFileListOfPentads[214].text == "}" 
    assert testFileListOfPentads[215].text == "}"
    assert testFileListOfPentads[216].text == "else"
    assert testFileListOfPentads[217].text == "{"
    assert testFileListOfPentads[218].text == "if (b == 37)"
    assert testFileListOfPentads[219].text == "{"
    assert testFileListOfPentads[220].text == "b = 38;"
    assert testFileListOfPentads[221].text == "for (c = 0; c < 100; c++)"
    assert testFileListOfPentads[222].text == "{"
    assert testFileListOfPentads[223].text == "if(a>b)"
    assert testFileListOfPentads[224].text == "{"
    assert testFileListOfPentads[225].text == "for (a>b)"
    assert testFileListOfPentads[226].text == "{"
    assert testFileListOfPentads[227].text == "if(a<b/4)"
    assert testFileListOfPentads[228].text == "{"
    assert testFileListOfPentads[229].text == "a = a + 3;"
    assert testFileListOfPentads[230].text == "}"
    assert testFileListOfPentads[231].text == "else"
    assert testFileListOfPentads[232].text == "{"
    assert testFileListOfPentads[233].text == "if (a<b/3)"
    assert testFileListOfPentads[234].text == "{"
    assert testFileListOfPentads[235].text == "a = a + 2;"
    assert testFileListOfPentads[236].text == "for (int i = 0; i < a; i++)"
    assert testFileListOfPentads[237].text == "{"
    assert testFileListOfPentads[238].text == "if (c < 200)"
    assert testFileListOfPentads[239].text == "{"
    assert testFileListOfPentads[240].text == "c = c + 10;"
    assert testFileListOfPentads[241].text == "}"
    assert testFileListOfPentads[242].text == "}"
    assert testFileListOfPentads[243].text == "}"
    assert testFileListOfPentads[244].text == "else"
    assert testFileListOfPentads[245].text == "{"
    assert testFileListOfPentads[246].text == "if(a<b/2)"
    assert testFileListOfPentads[247].text == "{"
    assert testFileListOfPentads[248].text == "if (b > 100)"
    assert testFileListOfPentads[249].text == "{"
    assert testFileListOfPentads[250].text == "if (a != 42)"
    assert testFileListOfPentads[251].text == "{"
    assert testFileListOfPentads[252].text == "a = a + 4;"
    assert testFileListOfPentads[253].text == "}"
    assert testFileListOfPentads[254].text == "}"
    assert testFileListOfPentads[255].text == "}"
    assert testFileListOfPentads[256].text == "}"
    assert testFileListOfPentads[257].text == "}"
    assert testFileListOfPentads[258].text == "}"
    assert testFileListOfPentads[259].text == "if(c * 2 == 280)"
    assert testFileListOfPentads[260].text == "{"
    assert testFileListOfPentads[261].text == "b = b + a;"
    assert testFileListOfPentads[262].text == "}"
    assert testFileListOfPentads[263].text == "else"
    assert testFileListOfPentads[264].text == "{"
    assert testFileListOfPentads[265].text == "b = b + b;"
    assert testFileListOfPentads[266].text == "}"
    assert testFileListOfPentads[267].text == "}"
    assert testFileListOfPentads[268].text == "else"
    assert testFileListOfPentads[269].text == "{"
    assert testFileListOfPentads[270].text == "if (b<c)"
    assert testFileListOfPentads[271].text == "{"
    assert testFileListOfPentads[272].text == "for (int j = 0; j < c; j++)"
    assert testFileListOfPentads[273].text == "{"
    assert testFileListOfPentads[274].text == "c = (a + j) * 10;"
    assert testFileListOfPentads[275].text == "}"
    assert testFileListOfPentads[276].text == "b = 100;"
    assert testFileListOfPentads[277].text == "}"
    assert testFileListOfPentads[278].text == "else"
    assert testFileListOfPentads[279].text == "{"
    assert testFileListOfPentads[280].text == "for (a > b)"
    assert testFileListOfPentads[281].text == "{"
    assert testFileListOfPentads[282].text == "if(b != a)"
    assert testFileListOfPentads[283].text == "{"
    assert testFileListOfPentads[284].text == "b = b+2;"
    assert testFileListOfPentads[285].text == "}"
    assert testFileListOfPentads[286].text == "else"
    assert testFileListOfPentads[287].text == "{"
    assert testFileListOfPentads[288].text == "if (a == b * 2)"
    assert testFileListOfPentads[289].text == "{"
    assert testFileListOfPentads[290].text == "a += 1;"
    assert testFileListOfPentads[291].text == "}"
    assert testFileListOfPentads[292].text == "}"
    assert testFileListOfPentads[293].text == "}"
    assert testFileListOfPentads[294].text == "}"
    assert testFileListOfPentads[295].text == "}"
    assert testFileListOfPentads[296].text == "}"
    assert testFileListOfPentads[297].text == "}"
    assert testFileListOfPentads[298].text == "else"
    assert testFileListOfPentads[299].text == "{"
    assert testFileListOfPentads[300].text == "b = 40;"
    assert testFileListOfPentads[301].text == "}"
    assert testFileListOfPentads[302].text == "}"
    assert testFileListOfPentads[303].text == "}"
    assert testFileListOfPentads[304].text == "}"
