class Token:
    def _init_(self, value, type):
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

Input_Tokens = []

with open("RPAL.txt", "r") as f:
    inputString = f.read()
    print(inputString)

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
            print(token)

        elif inputString[i].isdigit():
            temp = i
            while i + 1 < len(inputString) and inputString[i + 1].isdigit():
                i += 1
            token = inputString[temp : i + 1]
            print(token)

        elif inputString[i] in operator_symbol:
            token = inputString[i]
            print(token)

        elif inputString[i] == ' ' or inputString[i] == '\t' or inputString[i] == '\n':
            temp = i
            while i + 1 < len(inputString) and (inputString[i + 1] == ' ' or inputString[i + 1] == '\t' or inputString[i + 1] == '\n'):
                i += 1
            token = inputString[temp : i + 1]
            print(token)
        
        elif inputString[i] == '(':
            token = '('
            print(token)

        elif inputString[i] == ')':
            token = ')'
            print(token)

        elif inputString[i] == ';':
            token = ';'
            print(token)
        
        elif inputString[i] == ',':
            token = ','  
            print(token)

        
        elif inputString[i] == '\"':
            temp = i
            while(i + 1 < len(inputString) and (
                inputString[i + 1] == '\t'
                or inputString[i + 1] == '\n'
                or inputString[i + 1] == '\\'
                or inputString[i + 1] == '\"'

            )):
                i += 1
                 
            token = inputString[i :i + 1]
            print(token)

            
        i += 1
