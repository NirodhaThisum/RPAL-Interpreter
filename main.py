from Parsar import *

'''
file = sys.argv[1]
if len(sys.argv) == 3 and sys.argv[2] == "-ast":
    astFlag = sys.argv[2]
else:
    astFlag = ""
'''


file = "tests/vectorsum"
astFlag = "-ast"

scanner = RPAL_Scanner(file)  # Give the name of the file
tokens = scanner.Scanning()
myParser = ASTParser(tokens)
myParser.startParsing(astFlag)

root = myParser.stack[0]
stand = standardizer(root)

for i in range(10):
    stand.makeST(root)

'''
print(root.getVal(), "*********************************")


myParser.preOrderTraversal(root)

print("********************************")


'''
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


print("*********************************")
for i in setOfControlStruct:
    for j in i:
        print(j.value)
    print("*********")    


stand.cse_machine(setOfControlStruct)
