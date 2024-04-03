from MyScanner import Scanning
from MyScanner import Token

tokens = Scanning()


class ASTNode:
    def __init__(self, type, value):
        self.firstChild = None
        self.sibling = None
        self.value = value
        self.type = type  # This is the printing argument of AST node
        self.indentation = 0


class ASTParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0  # This is to track the current reading position
        self.stack = []

    def read(self, value, type):

        self.current_token = tokens[self.index]
        if (self.current_token.type != type) and (self.current_token.value != value):
            print("Error: Expected " + type +
                  " but got " + self.current_token.type)

        match type:
            case "<IDENTIFIER>":
                currentTokenType = "<ID:" + self.current_token.value + ">"
            case "<INTEGER>":
                currentTokenType = "<INT:" + self.current_token.value + ">"
            case "<STRING>":
                currentTokenType = "<STR:" + self.current_token.value + ">"
            case "<KEYWORD>":
                currentTokenType = self.current_token.value

        if self.current_token.type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"]:

            currentTokenType = (
                "<" + self.current_token.type + ":" + self.current_token.value + ">"
            )
            currentTokenValue = self.current_token.value
            terminalNode = ASTNode(currentTokenType, currentTokenValue)
            self.stack.append(terminalNode)

        # if self.current_token.value in ["true", "false", "nil", "dummy"]:
        #     stack.append(ASTNode(self.current_token.value))

        # print("reading : " + str(self.current_token.value))

        # Pick the next token
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]

    def testPrint(self):
        for token in self.stack:
            print(token.value, token.type)


myParser = ASTParser(tokens)
# for token in myParser.tokens:
#     print(token.value, token.type)

numberOfTokens = len(tokens)
for i in range(numberOfTokens):
    myParser.read()
myParser.testPrint()
