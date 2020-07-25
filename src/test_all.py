import os
import pytest
from pentadClass import pentadStruct
from LexicalAnalyser import spaceNormalizer, commentsEraser, stringReducer, multiLineManager, semicolonBasedChopper, doWhileConverter, whileLoopConverter
from CompleteAnalyser import mainCompleteAnalyser
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
    
