class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

number_of_Tokens = 0
punction = [")", "(", ";", ","]
operator_symbol = ["+", "-", "*", "<", ">", "&", ".", "@", "/", ":", "=",
                   "~", "|", "$", "!", "#", "%", "^", "_", "[", "]", "{", "}", '"', "`", "?"]
comment_elements = ['"', "\\", " ", "\t"]
keywords = ["let", "lambda", "where", "tau", "aug", "->", "or", "&", "not", "gr", "ge", "ls", "le", "eq", "ne", "+",
            "-", "neg", "*", "/", "**", "@", "gamma", "true", "false", "nil", "dummy", "within", "and", "rec", "=", "fcn_form"]
Input_Tokens = []
tokens = []

def Scanning():
    with open("RPAL.txt", "r") as f:
        inputString = f.read()
        # print(inputString)

        i = 0
        while i < len(inputString):

            if inputString[i].isalpha():
                temp = i
                while i + 1 < len(inputString) and (
                    (inputString[i + 1].isalpha())
                    or (inputString[i + 1].isdigit())
                    or (inputString[i + 1] == "_")
                ):
                    i += 1
                token = inputString[temp : i + 1]
                if token in keywords:
                    Input_Tokens.append(Token(token, token))
                else:
                    Input_Tokens.append(Token(token, "<IDENTIFIER>"))

            elif inputString[i].isdigit():
                temp = i
                while i + 1 < len(inputString) and inputString[i + 1].isdigit():
                    i += 1
                token = inputString[temp : i + 1]
                Input_Tokens.append(Token(token, "<INTEGER>"))

            elif inputString[i] == " " or inputString[i] == "\t" or inputString[i] == "\n":
                temp = i
                while i + 1 < len(inputString) and (
                    inputString[i + 1] == " "
                    or inputString[i + 1] == "\t"
                    or inputString[i + 1] == "\n"
                ):
                    i += 1
                token = inputString[temp : i + 1]
                Input_Tokens.append(Token(repr(token), "<DELETE>"))

            elif inputString[i] == "(":
                token = "("
                Input_Tokens.append(Token("(", "("))

            elif inputString[i] == ")":
                token = ")"
                Input_Tokens.append(Token(")", ")"))

            elif inputString[i] == ";":
                token = ";"
                Input_Tokens.append(Token(";", ";"))

            elif inputString[i] == ",":
                token = ","
                Input_Tokens.append(Token(",", ","))

            elif inputString[i] == '"':
                temp = i
                while (
                    i + 1 < len(inputString)
                    and (
                        inputString[i + 1] == "\t"
                        or inputString[i + 1] == "\n"
                        or inputString[i + 1] == "\\"
                        or inputString[i + 1] == "("
                        or inputString[i + 1] == ")"
                        or inputString[i + 1] == ";"
                        or inputString[i + 1] == ","
                        or inputString[i + 1] == " "
                        or inputString[i + 1].isalpha()
                        or inputString[i + 1].isdigit()
                        or inputString[i + 1] in operator_symbol
                    )
                    and inputString[i + 1] != '"'
                ):
                    i += 1
                if i + 1 < len(inputString) and inputString[i + 1] == '"':
                    i += 1
                    token = inputString[temp : i + 1]
                    Input_Tokens.append(Token(token, "<STRING>"))
            elif (
                inputString[i] == "/"
                and (i + 1 < len(inputString))
                and inputString[i + 1] == "/"
            ):
                temp = i
                while i + 1 < len(inputString) and (
                    (inputString[i + 1] in comment_elements)
                    or inputString[i + 1] in punction
                    or inputString[i + 1].isalpha()
                    or inputString[i + 1].isdigit()
                    or inputString[i + 1] in operator_symbol
                    and (not (inputString[i + 1] == "\n"))
                ):
                    i += 1

                if i + 1 < len(inputString) and inputString[i + 1] == "\n":
                    i += 1
                    # token = inputString[temp : i + 1]   #with last newline
                    token = inputString[temp:i]  # without newline
                    Input_Tokens.append(Token(token, "<DELETE>"))

            elif inputString[i] in operator_symbol:
                temp = i
                while i + 1 < len(inputString) and inputString[i + 1] in operator_symbol:
                    i += 1
                token = inputString[temp : i + 1]
                Input_Tokens.append(Token(token, token))

            i += 1

    # for token in Input_Tokens:
    #     print(token.value, token.type)

    # Screening
    Tokens = []

    for token in Input_Tokens:
        if token.type != "<DELETE>":
            Tokens.append(token)

    for token in Tokens:
        tokens.append((token.type, token.value))
    return Tokens

def Read(token):
    global next_token_of_type
    global current_token
    global next_token

    if len(tokens) == 0:
        return

    if token == next_token_of_type:
        if token in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"]:
            current_token = next_token
        next_token_of_type, next_token = tokens.pop(0)

def Build_Tree(token_type, children_count):

    if token_type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"]:
        if token_type == "<IDENTIFIER>":
            Token = "<ID:" + current_token + ">"
        if token_type == "<INTEGER>":
            Token = "<INT:" + str(current_token) + ">"
        if token_type == "<STRING>":
            Token = "<STR:" + current_token + ">"
        ast.append((Token, children_count))
    else:
        ast.append((token_type, children_count))

def Generate_Tree():
    global ast
    Postorder_AST = ast.copy()
    Postorder_AST.reverse()

    Preorder_AST = [None]
    current_index = 0
    current_depth = 0

    for node in Postorder_AST:
        child_count = node[1]
        token_val = node[0]

        Preorder_AST[current_index] = "." * current_depth + token_val
        current_depth += 1

        for j in range(child_count):
            current_index += 1
            Preorder_AST.insert(current_index, None)

        if child_count == 0:
            current_depth -= 1
            current_index -= 1
            while Preorder_AST[current_index] is not None and current_index > -1:
                current_depth -= 1
                current_index -= 1

    return Preorder_AST

def Print_AST():
    Preorder_AST = Generate_Tree()
    for node in Preorder_AST:
        print(node)

def Procedure_E():
    if next_token_of_type == "let":
        Read("let")
        Procedure_D()
        Read("in")
        Procedure_E()
        Build_Tree("let", 2)
    elif next_token_of_type == "fn":
        Read("fn")
        Procedure_Vb()
        n = 1
        while next_token_of_type in ["<IDENTIFIER>", "("]:
            Procedure_Vb()
            n += 1
        Read(".")
        Procedure_E()
        Build_Tree("lambda", n + 1)
    else:
        Procedure_Ew()

def Procedure_Ew():
    Procedure_T()
    if next_token_of_type == "where":
        Read("where")
        Procedure_Dr()
        Build_Tree("where", 2)

def Procedure_T():
    Procedure_Ta()
    if next_token_of_type == ",":
        Read(",")
        Procedure_Ta()
        n = 1
        while next_token_of_type == ",":
            n += 1
            Read(",")
            Procedure_Ta()
        Build_Tree("tau", n + 1)

def Procedure_Ta():
    Procedure_Tc()
    while next_token_of_type == "aug":
        Read("aug")
        Procedure_Tc()
        Build_Tree("aug", 2)

def Procedure_Tc():
    Procedure_B()
    if next_token_of_type == "->":
        Read("->")
        Procedure_Tc()
        Read("|")
        Procedure_Tc()
        Build_Tree("->", 3)

def Procedure_B():
    Procedure_Bt()
    while next_token_of_type == "or":
        Read("or")
        Procedure_Bt()
        Build_Tree("or", 2)

def Procedure_Bt():
    Procedure_Bs()
    while next_token_of_type == "&":
        Read("&")
        Procedure_Bs()
        Build_Tree("&", 2)


def Procedure_Bs():
    if next_token_of_type == "not":
        Read("not")
        Procedure_Bp()
        Build_Tree("not", 1)
    else:
        Procedure_Bp()

def Procedure_Bp():
    Procedure_A()
    match next_token_of_type:
        case "gr" | ">":
            Read(next_token_of_type)
            Procedure_A()
            Build_Tree("gr", 2)
        case "ge" | ">=":
            Read(next_token_of_type)
            Procedure_A()
            Build_Tree("ge", 2)
        case "ls" | "<":
            Read(next_token_of_type)
            Procedure_A()
            Build_Tree("ls", 2)
        case "le" | "<=":
            Read(next_token_of_type)
            Procedure_A()
            Build_Tree("le", 2)
        case "eq":
            Read(next_token_of_type)
            Procedure_A()
            Build_Tree("eq", 2)
        case "ne":
            Read(next_token_of_type)
            Procedure_A()
            Build_Tree("ne", 2)

def Procedure_A():
    if next_token_of_type == "+":
        Read("+")
        Procedure_At()
    elif next_token_of_type == "-":
        Read("-")
        Procedure_At()
        Build_Tree("neg", 1)
    else:
        Procedure_At()
        while next_token_of_type in ["+", "-"]:
            if next_token_of_type == "+":
                Read("+")
                Procedure_At()
                Build_Tree("+", 2)
            elif next_token_of_type == "-":
                Read("-")
                Procedure_At()
                Build_Tree("-", 2)

def Procedure_At():
    Procedure_Af()
    while next_token_of_type in ["*", "/"]:
        if next_token_of_type == "*":
            Read("*")
            Procedure_Af()
            Build_Tree("*", 2)
        elif next_token_of_type == "/":
            Read("/")
            Procedure_Af()
            Build_Tree("/", 2)

def Procedure_Af():
    Procedure_Ap()
    if next_token_of_type == "":
        Read("")
        Procedure_Af()
        Build_Tree("", 2)

def Procedure_Ap():
    Procedure_R()
    while next_token_of_type == "@":
        Read("@")
        Read("<IDENTIFIER>")
        Build_Tree("<IDENTIFIER>", 0)
        Procedure_R()
        Build_Tree("@", 2)

def Procedure_R():
    Procedure_Rn()
    while next_token_of_type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>", "true", "false", "nil", "(", "dummy"]:
        Procedure_Rn()
        Build_Tree("gamma", 2)

def Procedure_Rn():
    match next_token_of_type:
        case "<IDENTIFIER>":
            Read("<IDENTIFIER>")
            Build_Tree("<IDENTIFIER>", 0)
        case "<INTEGER>":
            Read("<INTEGER>")
            Build_Tree("<INTEGER>", 0)
        case "<STRING>":
            Read("<STRING>")
            Build_Tree("<STRING>", 0)
        case "true":
            Read("true")
            Build_Tree("true", 0)
        case "false":
            Read("false")
            Build_Tree("false", 0)
        case "nil":
            Read("nil")
            Build_Tree("nil", 0)
        case "(":
            Read("(")
            Procedure_E()
            Read(")")
        case "dummy":
            Read("dummy")
            Build_Tree("dummy", 0)

def Procedure_D():
    Procedure_Da()
    while next_token_of_type == "within":
        Read("within")
        Procedure_D()
        Build_Tree("within", 2)

def Procedure_Da():
    Procedure_Dr()
    n = 0
    while next_token_of_type == "and":
        Read("and")
        Procedure_Dr()
        n += 1
    if n > 0:
        Build_Tree("and", n + 1)


def Procedure_Dr():
    if next_token_of_type == "rec":
        Read("rec")
        Procedure_Db()
        Build_Tree("rec", 1)
    else:
        Procedure_Db()


def Procedure_Db():
    if next_token_of_type == "(":
        Read("(")
        Procedure_D()
        Read(")")
        n = 0
    if next_token_of_type == "<IDENTIFIER>":
        Procedure_Vl()
        if next_token_of_type == "=":
            Read("=")
            Procedure_E()
            Build_Tree("=", 2)
        else:
            Procedure_Vb()
            n = 1
            while next_token_of_type in ["<IDENTIFIER>", "("]:
                Procedure_Vb()
                n += 1
            Read("=")
            Procedure_E()
            Build_Tree("fcn_form", n + 2)


def Procedure_Vb():
    if next_token_of_type == "<IDENTIFIER>":
        Read("<IDENTIFIER>")
        Build_Tree("<IDENTIFIER>", 0)
    elif next_token_of_type == "(":
        Read("(")
        if next_token_of_type == "<IDENTIFIER>":
            Procedure_Vl()
            Read(")")
        else:
            Read(")")
            Build_Tree("()", 0)
    else:
        print("Error:error occurs near", next_token,
              " .IDENTIFIER or ')' expected.")

def Procedure_Vl():
    if next_token_of_type == "<IDENTIFIER>":
        Read("<IDENTIFIER>")
        Build_Tree("<IDENTIFIER>", 0)
        n = 0
        while next_token_of_type == ",":
            Read(",")
            Read("<IDENTIFIER>")
            Build_Tree("<IDENTIFIER>", 0)
            n += 1
        if n > 0:
            Build_Tree(",", n + 1)
    else:
        print("Error:error occurs near ", next_token, " .IDENTIFIER expected.")


Scanning()
# print(tokens)
next_token_of_type = ""
next_token = ""
current_token = ""
ast = []

Read("")
Procedure_E()
Print_AST()