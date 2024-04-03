from MyScanner import Scanning
from MyScanner import Token

tokens = Scanning()


class ASTNode:
    def __init__(self, type):
        self.firstChild = None
        self.sibling = None
        self.token = None
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

        if self.current_token.value != value and value != "UserDefined":
            print("Error: Expected " + type + " but got " + self.current_token.type)
            print("Error: Expected " + value + "but got " + self.current_token.value)
            return
        
        currentTokenType = ""
        match type:
            case "<IDENTIFIER>":
                currentTokenType = "<ID:" + self.current_token.value + ">"
            case "<INTEGER>":
                currentTokenType = "<INT:" + self.current_token.value + ">"
            case "<STRING>":
                currentTokenType = "<STR:" + self.current_token.value + ">"
            case "<KEYWORD>":
                currentTokenType = self.current_token.value
            case "<OPERATOR>":
                currentTokenType = self.current_token.value


        terminalNode = ASTNode(currentTokenType)
        self.stack.append(terminalNode)

        # Pick the next token
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]

    def buildTree(self, token, numOfChilds):
        # pass the transduction grammar value as the token
        parentNode = ASTNode(token)
        head = None
        for i in range(numOfChilds):
            child = self.stack.pop()
            child.sibling = head
            head = child
        parentNode.firstChild = head
        self.stack.append(parentNode)

    # Parsing Table

    # Expressions
    def E(self):
        match self.current_token.value:

            # E -> ’let’ D ’in’ E
            case "let":
                self.read("let", "<KEYWORD>")
                self.D()

                if self.current_token.value != "in":
                    print("Error: in is expected")
                    return

                self.read("in", "<KEYWORD>")
                self.E()
                print("E->let D in E")
                numberOfTerminals = 2
                self.buildTree("let", numberOfTerminals)

            # -> ’fn’ Vb+ ’.’ E
            case "fn":
                n = 0
                self.read("fn", "<KEYWORD>")

                while (
                    self.current_token.type == "<IDENTIFIER>"
                    or self.current_token.value == "("
                ):
                    self.Vb()
                    n += 1

                if n == 0:
                    print("E: at least one 'Vb' expected\n")
                    return

                if self.current_token.value != ".":
                    print("Error: . is expected")
                    return

                self.read(".", "<OPERATOR>")
                self.E()
                print("E->fn Vb . E")
                self.buildTree("lambda", n + 1)

            case _:
                self.Ew()
                print("E->Ew")

    def Ew(self):
        print("Ew")
        self.T()
        print("Ew->T")
        if self.current_token.value == "where":
            self.read("where", "<KEYWORD>")
            self.Dr()
            print("Ew->T where Dr")
            self.buildTree("where", 2)


    # Tuple Expressions
            
    def T(self):

        print("T")
        self.Ta()
        # print('T->Ta')

        n = 0
        while self.current_token.value == ",":
            self.read(",", "<OPERATOR>")
            self.Ta()
            n += 1
            print("T->Ta , Ta")

        if n > 0:
            self.buildTree("tau", n + 1)

        else:
            print("T->Ta")

    def testPrint(self):
        for token in self.stack:
            print(token.value, token.type)

    def VL(self):
        # Vl -> ’<IDENTIFIER>’ list ’,’

        if self.current_token.type == "<IDENTIFIER>":

            self.read()
            trees_to_pop = 0
            while self.current_token.value == ',':
                # Vl -> '<IDENTIFIER>' list ',' => ','?;
                self.read()
                if self.current_token.type != Tokernizer.TokenType.ID:
                    # Replace with appropriate error handling
                    print(" 572 VL: Identifier expected")
                self.read()
                print('VL->id , ?')

                trees_to_pop += 1
            print('498')
            if trees_to_pop > 0:
                # +1 for the first identifier
                self.buildTree(',', trees_to_pop + 1)


myParser = ASTParser(tokens)
# for token in myParser.tokens:
#     print(token.value, token.type)


myParser.current_token = tokens[0]
numberOfTokens = len(tokens)
myParser.E()
for i in myParser.stack:
    print(i)
# for i in range(numberOfTokens):
#     myParser.read()
# myParser.testPrint()
