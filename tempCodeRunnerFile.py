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
