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