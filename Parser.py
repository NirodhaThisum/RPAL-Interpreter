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
        # value of identifier, string, and integer are user defined

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
            case _:
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

    def E(self):
        # E -> ’let’ D ’in’ E => ’let’
        if self.current_token.value == "let":
            self.read("let", "<KEYWORD>")
            self.D()
            self.read("in", "<KEYWORD>")
            self.E()
            self.buildTree("let", 2)
        # E -> ’fn’ Vb+ ’.’ E => ’lambda’
        elif self.current_token.value == "fn":
            self.read("fn", "<KEYWORD>")
            self.Vb()
            n = 1
            while self.current_token.value in ["<IDENTIFIER>", "("]:
                self.Vb()
                n += 1
            self.read(".", "<OPERATOR>")
            self.E()
            self.buildTree("lambda", n + 1)
        # E -> Ew
        else:
            Ew()


    def Ew(self):
        self.T()  # E -> T
        # Ew -> T ’where’ Dr => ’where’
        if self.current_token.value == "where":
            self.read("where", "<KEYWORD>")
            self.Dr()
            self.buildTree("where", 2)


    def T(self):
        self.Ta()  # E -> Ta
        # T -> Ta ( ’,’ Ta )+ => ’tau’
        if self.current_token.value == ",":
            self.read(",", ",")
            self.Ta()
            n = 1  # track the number pf repitition
            while self.current_token.value == ",":
                n += 1
                self.read(",", ",")
                self.Ta()
            self.buildTree("tau", n + 1)


    def Ta(self):
        self.Tc()  # E -> Tc
        # Ta -> Ta ’aug’ Tc => ’aug’
        while self.current_token.value == "aug":
            self.read("aug", "<KEYWORD>")
            self.Tc()
            self.buildTree("aug", 2)


    def Tc(self):
        self.B()  # E -> B
        # Tc -> B ’->’ Tc ’|’ Tc => ’->’
        if self.current_token.value == "->":
            self.read("->","<OPERATOR>")
            self.Tc()
            self.read("|", )
            self.Tc()
            self.buildTree("->", 3)


    def B(self):
        self.Bt()  # E -> Bt
        # B ->B’or’ Bt => ’or’
        while self.current_token.value == "or":
            self.read("or")
            self.Bt()
            self.buildTree("or", 2)


    def Bt(self):
        self.Bs()  # E -> Bs
        # Bt -> Bt ’&’ Bs => ’&’
        while self.current_token.value == "&":
            self.read("&")
            self.Bs()
            self.buildTree("&", 2)


    def Bs(self):
        # Bs -> ’not’ Bp => ’not’
        if self.current_token.value == "not":
            self.read("not")
            self.Bp()
            self.buildTree("not", 1)
        else:
            # E -> Bp
            self.Bp()


    def Bp(self):
        self.A()  # E -> A
        # Bp -> A (’gr’ | ’>’ ) A => ’gr’
        if self.current_token.value in ["gr", ">"]:
            self.read(self.current_token.value)
            self.A()
            self.buildTree("gr", 2)
        # Bp -> A (’ge’ | ’>=’) A => ’ge’
        elif self.current_token.value in ["ge", ">="]:
            self.read(self.current_token.value)
            self.A()
            self.buildTree("ge", 2)
        # Bp -> A (’ls’ | ’<’ ) A => ’ls’
        elif self.current_token.value in ["ls", "<"]:
            self.read(self.current_token.value)
            self.A()
            self.buildTree("ls", 2)
        # Bp -> A (’le’ | ’<=’) A => ’le’
        elif self.current_token.value in ["le", "<="]:
            self.read(self.current_token.value)
            self.A()
            self.buildTree("le", 2)
        # Bp -> A ’eq’ A => ’eq’
        elif self.current_token.value == "eq":
            self.read(self.current_token.value)
            self.A()
            self.buildTree("eq", 2)
        # Bp -> A ’ne’ A => ’ne’
        elif self.current_token.value == "ne":
            self.read(self.current_token.value)
            self.A()
            self.buildTree("ne", 2)


    def A(self):
        # A -> ’+’ At
        if self.current_token.value == "+":
            self.read("+")
            self.At()
        # A -> ’-’ At => ’neg’
        elif self.current_token.value == "-":
            self.read("-")
            self.At()
            self.buildTree("neg", 1)
        else:
            self.At()  # A -> At
            while self.current_token.value in ["+", "-"]:
                # A ->A’+’ At => ’+’
                if self.current_token.value == "+":
                    self.read("+")
                    self.At()
                    self.buildTree("+", 2)
                # A -> A ’-’ At => ’-’
                elif self.current_token.value == "-":
                    self.read("-")
                    self.At()
                    self.buildTree("-", 2)


    def At(self):
        self.Af()  # A -> Af
        while self.current_token.value in ["*", "/"]:
            # At -> At ’*’ Af => ’*’
            if self.current_token.value == "*":
                self.read("*")
                self.Af()
                self.buildTree("*", 2)
            # At -> At ’/’ Af => ’/’
            elif self.current_token.value == "/":
                self.read("/")
                self.Af()
                self.buildTree("/", 2)


    def Af(self):
        self.Ap()  # Af -> Ap
        # Af -> Ap ’**’ Af => ’**’
        if self.current_token.value == "**":
            self.read("**")
            self.Af()
            self.buildTree("**", 2)


    def Ap(self):
        self.R()  # Ap -> R
        # Ap -> Ap ’@’ ’<IDENTIFIER>’ R => ’@’
        while self.current_token.value == "@":
            self.read("@")
            self.read("<IDENTIFIER>")
            self.buildTree(self.current_token.value, 0)
            self.R()
            self.buildTree("@", 2)


    def R(self):
        self.Rn()  # R -> Rn
        # R ->R Rn => ’gamma’
        while self.current_token.value in [
            "<IDENTIFIER>",
            "<INTEGER>",
            "<STRING>",
            "true",
            "false",
            "nil",
            "(",
            "dummy",
        ]:
            self.Rn()
            self.buildTree("gamma", 2)


    def Rn(self):
        # Rn -> ’<IDENTIFIER>’
        if self.current_token.type == "<IDENTIFIER>":
            self.read("<IDENTIFIER>")
            self.buildTree(self.current_token.value, 0)
        # Rn -> ’<INTEGER>’
        elif self.current_token.type == "<INTEGER>":
            self.read("<INTEGER>")
            self.buildTree("<INTEGER>", 0)
        # Rn -> ’<STRING>’
        elif self.current_token.type == "<STRING>":
            self.read("<STRING>")
            self.buildTree("<STRING>", 0)
        # Rn -> ’true’ => ’true’
        elif self.current_token.value == "true":
            self.read("true")
            self.vbuildTree("true", 0)
        # Rn -> ’false’ => ’false’
        elif self.current_token.value == "false":
            self.read("false")
            self.buildTree("false", 0)
        # Rn -> ’nil’ => ’nil’
        elif self.current_token.value == "nil":
            self.read("nil")
            self.buildTree("nil", 0)
        # Rn -> ’(’ E ’)’
        elif self.current_token.value == "(":
            self.read("(")
            self.E()
            self.read(")")
        # Rn -> ’dummy’ => ’dummy’
        elif self.current_token.value == "dummy":
            self.read("dummy")
            self.buildTree("dummy", 0)


    def D(self):
        self.Da()  # D -> Da
        # D -> Da ’within’ D => ’within’
        while self.current_token.value == "within":
            self.read("within")
            self.D()
            self.buildTree("within", 2)


    def Da(self):
        self.Dr()  # Da -> Dr
        n = 0  # keep track of repitation of Dr
        # Da -> Dr ( ’and’ Dr )+ => ’and’
        while self.current_token.value == "and":
            self.read("and")
            self.Dr()
            n += 1
        if n > 0:
            self.buildTree("and", n + 1)


    def Dr(self):
        # Dr -> ’rec’ Db => ’rec’
        if self.current_token.value == "rec":
            self.read("rec")
            self.Db()
            self.buildTree("rec", 1)
        else:
            # Dr -> Db
            self.Db()


    def Db(self):
        # Db -> ’(’ D ’)’
        if self.current_token.value == "(":
            self.read("(")
            self.D()
            self.read(")")
            n = 0
        if self.current_token.type == "<IDENTIFIER>":
            # Db -> Vl ’=’ E => ’=’
            self.Vl()
            if self.current_token.value == "=":
                self.read("=")
                self.E()
                self.buildTree("=", 2)
            else:
                # Db-> ’<IDENTIFIER>’ Vb+ ’=’ E => ’fcn_form’
                self.Vb()
                n = 1
                while self.current_token.value in ["<IDENTIFIER>", "("]:
                    self.Vb()
                    n += 1
                self.read("=")
                self.E()
                self.buildTree("fcn_form", n + 2)
        # else:
        #     print("Error:error occurs near", Next_Token, " '(' or IDENTIFIER expected.")


    def Vb(self):
        # Vb -> ’<IDENTIFIER>’
        if self.current_token.type == "<IDENTIFIER>":
            self.read("<IDENTIFIER>")
            self.buildTree(self.current_token.value, 0)
        elif self.current_token.value == "(":
            self.read("(")
            # Vb -> ’(’ Vl ’)’
            if self.current_token.type == "<IDENTIFIER>":
                self.Vl()
                self.read(")")
            # Vb -> ’(’ ’)’
            else:
                self.read(")")
                self.buildTree("()", 0)
        # else:
            # Handle Error
            # print("Error:error occurs near", Next_Token, " .IDENTIFIER or ')' expected.")


    def Vl(self):
        # Vl -> ’<IDENTIFIER>’ list ’,’ => ’,’?
        if self.current_token.type == "<IDENTIFIER>":
            self.read("<IDENTIFIER>")
            self.buildTree(self.current_token.value, 0)
            n = 0
            while self.current_token.value == ",":
                self.read(",")
                self.read("<IDENTIFIER>")
                self.buildTree(self.current_token.value, 0)
                n += 1
            if n > 0:
                self.buildTree(",", n + 1)
        # else:
        #     # handle error
        #     print("Error:error occurs near ", Next_Token, " .IDENTIFIER expected.")

'''
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
*/
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

    #   Ew -> T ’where’ Dr
    #      -> T;
    def Ew(self):
        self.T()
        if self.current_token.value == "where":
            self.read("where", "<KEYWORD>")
            self.Dr()
            print("Ew->T where Dr")
            self.buildTree("where", 2)

    # Tuple Expressions

    #     T -> Ta ( ’,’ Ta )+
    #       -> Ta ;
    def T(self):
        self.Ta()
        n = 0
        while self.current_token.value == ",":
            self.read(",", ",")
            self.Ta()
            n += 1
            print("T->Ta , Ta")

        if n > 0:
            self.buildTree("tau", n + 1)

        else:
            print("T->Ta")

    #     Ta -> Ta ’aug’ Tc
    #        -> Tc ;
    def Ta(self):
        self.Tc()
        while self.current_token.value == "aug":
            self.read("aug", "<KEYWORD>")
            self.Tc()
            self.buildTree("aug", 2)

    #     Ta -> Ta ’aug’ Tc
    #        -> Tc ;
    def Tc(self):
        self.B()
        if self.current_token.type == "->":
            self.read("->", "<OPERATOR>")
            self.Tc()

            if self.current_token.value != "|":
                print("Error: | is expected")
                return
            self.read("|", "<OPERATOR>")
            self.Tc()
            self.buildTree("->", 3)

    # Boolean Expressions

    #      B -> B ’or’ Bt
    #        -> Bt
    def B(self):
        self.Bt()
        while self.current_token.value == "or":
            self.read("or", "<KEYWORD>")
            self.Bt()
            self.buildTree("or", 2)

    #      Bt -> Bt ’&’ Bs
    #         -> Bs ;
    def Bt(self):
        self.Bs()
        while self.current_token.value == "&":
            self.read("&", "<KEYWORD>")
            self.Bs()
            self.buildTree("&", 2)

    #      Bs -> ’not’ Bp
    #         -> Bp
    def Bs(self):
        if self.current_token.value == "not":
            self.read("not", "<KEYWORD>")
            self.Bp()
            self.buildTree("not", 1)
        else:
            self.Bp()
# #######################################################################
    # Bp -> A (’gr’ | ’>’ ) A
    # -> A (’ge’ | ’>=’) A
    # -> A (’ls’ | ’<’ ) A
    # -> A (’le’ | ’<=’) A
    # -> A ’eq’ A
    # -> A ’ne’ A
    # -> A ;
 '''  

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
