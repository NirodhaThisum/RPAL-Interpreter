
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
