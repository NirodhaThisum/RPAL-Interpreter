class MyCustomError(Exception):
    pass


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type


number_of_Tokens = 0

punction = [")", "(", ";", ","]

operator_symbol = [
    "+",
    "-",
    "*",
    "<",
    ">",
    "&",
    ".",
    "@",
    "/",
    ":",
    "=",
    "~",
    "|",
    "$",
    "!",
    "#",
    "%",
    "^",
    "_",
    "[",
    "]",
    "{",
    "}",
    '"',
    "`",
    "?",
]


comment_elements = ['"', "\\", " ", "\t"]


Input_Tokens = []

with open("RPAL.txt", "r") as f:
    inputString = f.read()
    # print(inputString)

    i = 0
    while i < len(inputString):

        if inputString[i].isalpha():
            temp = i
            # while i + 1 < len(inputString) and inputString[i + 1].isalpha():
            while i + 1 < len(inputString) and (
                (inputString[i + 1].isalpha())
                or (inputString[i + 1].isdigit())
                or (inputString[i + 1] == "_")
            ):
                i += 1
            token = inputString[temp : i + 1]
            Input_Tokens.append(Token(token, "<IDENTIFIER>"))
            print(token)

        elif inputString[i].isdigit():
            temp = i
            while i + 1 < len(inputString) and inputString[i + 1].isdigit():
                i += 1
            token = inputString[temp : i + 1]
            Input_Tokens.append(Token(token, "<INTEGER>"))
            print(token)

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
            print(token)

        elif inputString[i] == "(":
            token = "("
            Input_Tokens.append(Token("(", "("))
            print(token)

        elif inputString[i] == ")":
            token = ")"
            Input_Tokens.append(Token(")", ")"))
            print(token)

        elif inputString[i] == ";":
            token = ";"
            Input_Tokens.append(Token(";", ";"))
            print(token)

        elif inputString[i] == ",":
            token = ","
            Input_Tokens.append(Token(",", ","))
            print(token)

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
                print(token)

            else:
                raise MyCustomError('need " ')

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
            # token = inputString[temp: i + 1]
            # Input_Tokens.append(Token(token, "<DELETE>"))
            print(token)

            if i + 1 < len(inputString) and inputString[i + 1] == "\n":
                i += 1
                # token = inputString[temp : i + 1]   #with last newline
                token = inputString[temp:i]  # without newline
                Input_Tokens.append(Token(token, "<DELETE>"))
                print(token)

            else:
                raise MyCustomError("need to end with newline")

        elif inputString[i] in operator_symbol:
            temp = i
            while i + 1 < len(inputString) and inputString[i + 1] in operator_symbol:
                i += 1
            token = inputString[temp : i + 1]
            Input_Tokens.append(Token(token, "<OPERATOR>"))
            print(token)

        i += 1


# for token in Input_Tokens:
#     print(token.value, token.type)


# Screening
Tokens = []

for token in Input_Tokens:
    if token.type != "<DELETE>":
        Tokens.append(token)


for token in Tokens:
    print(token.value, token.type)
