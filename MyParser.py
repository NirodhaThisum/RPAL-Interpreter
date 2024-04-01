class Token:
    def __init__(self):
        self.type = ""
        self.val = ""

    # Set type of token
    def setType(self, sts):
        self.type = sts

    # Set value of token
    def setVal(self, str):
        self.val = str

    # Get type of token
    def getType(self):
        return self.type

    # Get value of token
    def getVal(self):
        return self.val

    # Define inequality operator
    def __ne__(self, t):
        return self.type != t.type

binary_operators = ["+", "-", "*", "/", "**", "gr", "ge", "<",
                    "<=", ">", ">=", "ls", "le", "eq", "ne", "&", "or", "><"]


class tree:
    def __init__(self):
        self.value = None   # Value of node
        self.type = None  # Type of node
        self.left = None  # Left child
        self.right = None  # Right child

    # Set type of node
    def setType(self, typ):
        self.type = typ

    # Set value of node
    def setVal(self, value):
        self.value = value

    # Get type of node
    def getType(self):
        return self.type

    # Get value of node
    def getVal(self):
        return self.value

    # Create node with value and type
    @staticmethod
    def createNode(value, typ):
        t = tree()
        t.setVal(value)
        t.setType(typ)
        t.left = None
        t.right = None
        return t

    # Create node with tree object
    @staticmethod
    def createNodeFromTree(x):
        t = tree()
        t.setVal(x.getVal())
        t.setType(x.getType())
        t.left = x.left
        t.right = None
        return t

    # Print syntax tree
    def print_tree(self, no_of_dots):
        n = 0
        while n < no_of_dots:
            print(".", end="")
            n += 1

        # If node type is ID, STR, or INT, print <type:val>
        if self.type == "ID" or self.type == "STR" or self.type == "INT":
            print("<", end="")
            print(self.type, end=":")

        # If node type is BOOL, NIL, or DUMMY, print <val>
        if self.type == "BOOL" or self.type == "NIL" or self.type == "DUMMY":
            print("<", end="")

        print(self.value, end="")

        # If node type is ID, STR, or INT, print >
        if self.type == "ID" or self.type == "STR" or self.type == "INT":
            print(">", end="")

        # If node type is BOOL, NIL, or DUMMY, print >
        if self.type == "BOOL" or self.type == "NIL" or self.type == "DUMMY":
            print(">", end="")

        print()

        # Print left and right subtrees
        if self.left is not None:
            self.left.print_tree(no_of_dots + 1)

        if self.right is not None:
            self.right.print_tree(no_of_dots)


tree_obj = tree.createNode("value", "type")
tree_obj.print_tree(0)


operators = ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', '!', '#', '%',
             '^', '_', '[', ']', '{', '}', '"', '`', '?']
keys = ["let", "fn", "in", "where", "aug", "or", "not", "true", "false", "nil", "dummy", "within",
        "and", "rec", "gr", "ge", "ls", "le", "eq", "ne"]


class parser:
    def __init__(self, read_array, i, size, af):
        self.readnew = read_array[:10000]
        self.index = i
        self.sizeOfFile = size
        self.astFlag = af
        self.nextToken = Token()

    def isReservedKey(self, s):
        return s in keys

    def isOperator(self, ch):
        return ch in operators

    def isAlpha(self, ch):
        return ch.isalpha()

    def isDigit(self, ch):
        return ch.isdigit()

    def isBinaryOperator(self, op):
        binary_operators = ['+', '-', '*', '/', '%', '<', '>',
                            '=', '==', '<=', '>=', '!=', '&&', '||', '&', '|', '^']
        return op in binary_operators

    def isNumber(self, s):
        return s.isdigit()

    def read(self, val, type):
        if val != self.nextToken.getVal() or type != self.nextToken.getType():
            print("Parse error: Expected", "\"" + val + "\"", "but",
                  "\"" + self.nextToken.getVal() + "\"", "was there")
            exit(0)

        if type == "ID" or type == "INT" or type == "STR":
            self.buildTree(val, type, 0)

        self.nextToken = self.getToken(self.readnew)

        while self.nextToken.getType() == "DELETE":
            self.nextToken = self.getToken(self.readnew)

    def procedure_E(self):
        # E -> ’let’ D ’in’ E
        if self.nextToken.getVal() == "let":
            # read("let", "KEYWORD")
            procedure_D()
            # read("in", "KEYWORD")  # read in
            self.procedure_E()
            # buildTree("let", "KEYWORD", 2)

        # E -> ’fn’ Vb+ ’.’ E
        elif self.nextToken.getVal() == "fn":
            n = 0
            # read("fn", "KEYWORD")
            while self.nextToken.getType() == "ID" or self.nextToken.getVal() == "(":
                self.procedure_Vb()
                n += 1
            # read(".", "OPERATOR")
            self.procedure_E()
            # buildTree("lambda", "KEYWORD", n + 1)

        # E -> Ew
        else:
            self.procedure_Ew()

    def procedure_Ew(self):
        self.procedure_T()
        if self.nextToken.getVal() == "where":
            # read("where", "KEYWORD")
            procedure_Dr()
            # buildTree("where", "KEYWORD", 2)

    def procedure_T(self):
        procedure_Ta()

        n = 1
        while self.nextToken.getVal() == ",":
            n += 1
            # read(",", "PUNCTION")
            procedure_Ta()

        if n > 1:
            # buildTree("tau", "KEYWORD", n)


    def procedure_Ta():
        procedure_Tc()

        while nextToken.getVal() == "aug":
            read("aug", "KEYWORD")
            procedure_Tc()
            buildTree("aug", "KEYWORD", 2)


def procedure_Tc():
    procedure_B()

    if nextToken.getVal() == "->":
        read("->", "OPERATOR")
        procedure_Tc()
        read("|", "OPERATOR")
        procedure_Tc()
        buildTree("->", "KEYWORD", 3)


def procedure_B():
    procedure_Bt()

    while nextToken.getVal() == "or":
        read("or", "KEYWORD")
        procedure_Bt()
        buildTree("or", "KEYWORD", 2)


def procedure_Bt():
    procedure_Bs()

    while nextToken.getVal() == "&":
        read("&", "OPERATOR")
        procedure_Bs()
        buildTree("&", "KEYWORD", 2)


def procedure_Bs():
    if nextToken.getVal() == "not":
        read("not", "KEYWORD")
        procedure_Bp()
        buildTree("not", "KEYWORD", 1)
    else:
        procedure_Bp()


def procedure_Bp():
    procedure_A()
    temp = nextToken.getVal()
    temp2 = nextToken.getType()

    if temp in ["gr", ">", "ge", ">=", "ls", "<", "le", "<=", "eq", "ne"]:
        read(temp, temp2)
        procedure_A()
        buildTree(temp, "KEYWORD", 2)
    elif temp == "ne":
        read(temp, temp2)
        procedure_A()
        buildTree(temp, "KEYWORD", 2)


def procedure_A():
    if nextToken.getVal() == "+":
        read("+", "OPERATOR")
        procedure_At()
    elif nextToken.getVal() == "-":
        read("-", "OPERATOR")
        procedure_At()
        buildTree("neg", "KEYWORD", 1)
    else:
        procedure_At()

    while nextToken.getVal() in ["+", "-"]:
        temp = nextToken.getVal()
        read(temp, "OPERATOR")
        procedure_At()
        buildTree(temp, "OPERATOR", 2)


def procedure_At():
    procedure_Af()

    while nextToken.getVal() in ["*", "/"]:
        temp = nextToken.getVal()
        read(temp, "OPERATOR")
        procedure_Af()
        buildTree(temp, "OPERATOR", 2)


def procedure_Af():
    procedure_Ap()

    if nextToken.getVal() == "**":
        read("**", "OPERATOR")
        procedure_Af()
        buildTree("**", "KEYWORD", 2)


def procedure_Ap():
    procedure_R()
    while nextToken.getVal() == "@":
        read("@", "OPERATOR")
        if nextToken.getType() != "ID":
            print("Exception: UNEXPECTED_TOKEN")
        else:
            read(nextToken.getVal(), "ID")
            procedure_R()
            buildTree("@", "KEYWORD", 3)


def procedure_R():
    procedure_Rn()
    while nextToken.getType() in ["ID", "INT", "STR"] or nextToken.getVal() in ["true", "false", "nil", "(", "dummy"]:
        procedure_Rn()
        buildTree("gamma", "KEYWORD", 2)


def procedure_Rn():
    if nextToken.getType() in ["ID", "INT", "STR"]:
        read(nextToken.getVal(), nextToken.getType())
    elif nextToken.getVal() in ["true", "false", "nil"]:
        read(nextToken.getVal(), "KEYWORD")
        buildTree(nextToken.getVal(), "BOOL", 0)
    elif nextToken.getVal() == "(":
        read("(", "PUNCTION")
        procedure_E()
        read(")", "PUNCTION")
    elif nextToken.getVal() == "dummy":
        read("dummy", "KEYWORD")
        buildTree("dummy", "DUMMY", 0)


def procedure_D():
    procedure_Da()
    if nextToken.getVal() == "within":
        read("within", "KEYWORD")
        procedure_Da()
        buildTree("within", "KEYWORD", 2)


def procedure_Da():
    procedure_Dr()

    n = 1
    while nextToken.getVal() == "and":
        n += 1
        read("and", "KEYWORD")
        procedure_Dr()
    if n > 1:
        buildTree("and", "KEYWORD", n)


def procedure_Dr():
    if nextToken.getVal() == "rec":
        read("rec", "KEYWORD")
        procedure_Db()
        buildTree("rec", "KEYWORD", 1)
    else:
        procedure_Db()


def procedure_Db():
    if nextToken.getVal() == "(":
        read("(", "PUNCTION")
        procedure_D()
        read(")", "PUNCTION")
    elif nextToken.getType() == "ID":
        read(nextToken.getVal(), "ID")
        n = 1
        if nextToken.getVal() in ["=", ","]:
            while nextToken.getVal() == ",":
                read(",", "PUNCTION")
                read(nextToken.getVal(), "ID")
                n += 1
            if n > 1:
                buildTree(",", "KEYWORD", n)
            read("=", "OPERATOR")
            procedure_E()
            buildTree("=", "KEYWORD", 2)
        else:
            while nextToken.getType() == "ID" or nextToken.getVal() == "(":
                procedure_Vb()
                n += 1
            read("=", "OPERATOR")
            procedure_E()
            buildTree("function_form", "KEYWORD", n + 1)


def procedure_Vb():
    if nextToken.getType() == "ID":
        read(nextToken.getVal(), "ID")
    elif nextToken.getVal() == "(":
        read("(", "PUNCTION")
        if nextToken.getVal() == ")":
            read(")", "PUNCTION")
            buildTree("()", "KEYWORD", 0)
        else:
            procedure_Vl()
            read(")", "PUNCTION")


def procedure_Vl():
    n = 1
    read(nextToken.getVal(), "ID")

    while nextToken.getVal() == ",":
        read(",", "PUNCTION")
        read(nextToken.getVal(), "ID")
        n += 1
    if n > 1:
        buildTree(",", "KEYWORD", n)



read_array = ["let", "x", "=", 5]
i = 0
size = len(read_array)
af = 1
parser_obj = parser(read_array, i, size, af)
print(parser_obj.isReservedKey("some"))
for i in range(size):
    print(read_array[i])
    print(parser_obj.isReservedKey(read_array[i]))
    print(parser_obj.isOperator(read_array[i]))
#     print(parser_obj.isAlpha(read_array[i]))
#     print(parser_obj.isDigit(read_array[i]))
    print(parser_obj.isBinaryOperator(read_array[i]))
#     print(parser_obj.isNumber(read_array[i]))
    print("")
