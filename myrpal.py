from Parsar import *
import sys
hasParsingError = False
hasCSEError = False
hasInputError = False
astFlag = ""

file = sys.argv[1]
if len(sys.argv) == 3 and sys.argv[2] == "-ast":
    astFlag = sys.argv[2]
elif len(sys.argv) == 3 and sys.argv[2] != "-ast":
    hasInputError = True
    astFlag = "invalid"
elif len(sys.argv) == 2:
    astFlag = ""
else:
    hasInputError = True
    astFlag = "invalid"


#For testing purposes
# file = "tests/wsum2"
# astFlag = "-ast"

scanner = RPAL_Scanner(file)  # Give the name of the file
tokens = scanner.Scanning()

myParser = ASTParser(tokens)
myParser.startParsing(astFlag)
hasParsingError = myParser.isAnError()

if not hasInputError or hasParsingError:
    root = myParser.stack[0]
    stand = standardizer(root)

    for i in range(10):
        stand.makeST(root)

    
    # Printing Standaradize tree for testing purposes
    # print(root.getVal(), "*********************************")
    # myParser.preOrderTraversal(root)
    # print("********************************")

    
    controlStructureArray = [[None for _ in range(200)] for _ in range(200)]
    stand.createControlStructures(root, controlStructureArray)

    size = 0
    while controlStructureArray[size][0] is not None:
        size += 1

    setOfControlStruct = []
    for x in range(size):
        temp = []
        for y in range(200):
            if controlStructureArray[x][y] is not None:
                temp.append(controlStructureArray[x][y])
        setOfControlStruct.append(temp)


    # print("*********************************")
    # for i in setOfControlStruct:
    #     for j in i:
    #         print(j.value)
    #     print("*********")    

    try:
        stand.cse_machine(setOfControlStruct)
    except Exception as e:
        print("CSE machine error")
        print(e)

elif hasParsingError:
    print("There is an Error in parsing. Check syntax of the program.")

else:
    print("Input Format is Wrong")
    print("Input format ==>  python .\\myrpal.py file_name")
    print("To print the AST use -ast flag at the end of the command.")
