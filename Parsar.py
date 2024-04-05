from MyScanner import RPAL_Scanner
from MyScanner import Token

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
        self.prevToken = None
        self.errorExist = False

    def read(self, value, type):
        # value of identifier, string, and integer are "UserDefined"     
        self.current_token = tokens[self.index]

        if self.current_token.value != value and value != "UserDefined":
            self.errorExist = True
            return

        # Pick the next token
        self.prevToken = self.current_token
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
          self.current_token.value = self.prevToken.value
          self.current_token.type = ""


    def preOrderTraversal(self, node, depth=0):
        if node is not None:
            print("." * depth + node.type)  # Prepend dots based on depth
            self.preOrderTraversal(
                node.firstChild, depth + 1
            )  # Visit the left child with increased depth
            self.preOrderTraversal(
                node.sibling, depth
            )  # Visit the right sibling with the same depth

    def startParsing(self):
        self.current_token = tokens[0]
        self.E()
        if self.errorExist:
            print("There is an Error")
        else:
            self.preOrderTraversal(self.stack[0])

    def buildTree(self, token, numOfChilds):
        # pass the transduction grammar value as the token
        parentNode = ASTNode(token)
        head = None
        for i in range(numOfChilds):
            if (
                len(self.stack) != 0
            ):  
                
                # If the grammar rules are correct the if statement is optional
     
                child = self.stack.pop()
                child.sibling = head
                head = child
            else:
                print("There is an error in code")
                self.errorExist = True
        parentNode.firstChild = head
        self.stack.append(parentNode)


    # Parsing Table

    def E(self):
        # E -> 'let' D 'in     E => 'let'
        if self.current_token.value == "let":
            self.read("let", "<KEYWORD>")
            self.D()

            if self.current_token.value != "in":
                print("Error: expected in")
                self.errorExist = True
                return
            
            self.read("in", "<KEYWORD>")
            self.E()
            self.buildTree("let", 2)

        # E -> 'fn' Vb+ '.' E => 'lambda'
        elif self.current_token.value == "fn":
            self.read("fn", "<KEYWORD>")
            self.Vb()
            n = 1
            while self.current_token.value in ["<IDENTIFIER>", "("]:
                self.Vb()
                n += 1
            if self.current_token.value != ".":
                print("Error: expected .")
                self.errorExist = True
                return
            self.read(".", "<OPERATOR>")
            self.E()
            self.buildTree("lambda", n + 1)

        # E -> Ew
        else:
            self.Ew()

    def Ew(self):
        self.T()  # E -> T
        # Ew -> T 'where' Dr => 'where'
        if self.current_token.value == "where":

            self.read("where", "<KEYWORD>")
            self.Dr()
            self.buildTree("where", 2)


    def T(self):
        self.Ta()  # E -> Ta
        # T -> Ta ( ',' Ta )+ => 'tau'
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
        # Ta -> Ta 'aug' Tc => 'aug'
        while self.current_token.value == "aug":
            self.read("aug", "<KEYWORD>")
            self.Tc()
            self.buildTree("aug", 2)
        

    def Tc(self):
        self.B()  # E -> B
        # Tc -> B '->' Tc '|' Tc => '->'
        if self.current_token.value == "->":
            self.read("->", "<OPERATOR>")
            self.Tc()
            if self.current_token.value != "|":
                print("Error: expected |")
                self.errorExist = True
                return
            self.read("|", "<OPERATOR>")
            self.Tc()
            self.buildTree("->", 3)


    def B(self):
        self.Bt()  # E -> Bt
        # B ->B'or' Bt => 'or'
        while self.current_token.value == "or":
            self.read("or", "<OPERATOR>")
            self.Bt()
            self.buildTree("or", 2)

    def Bt(self):
        self.Bs()  # E -> Bs
        # Bt -> Bt '&' Bs => '&'
        while self.current_token.value == "&":
            self.read("&", "<OPERATOR>")
            self.Bs()
            self.buildTree("&", 2)

    def Bs(self):
        # Bs -> 'not' Bp => 'not'
        if self.current_token.value == "not":
            self.read("not", "<OPERATOR>")
            self.Bp()
            self.buildTree("not", 1)
        else:
            # E -> Bp
            self.Bp()

    def Bp(self):
        self.A()  # E -> A
        # Bp -> A ('gr' | '>' ) A => 'gr'
        if self.current_token.value in ["gr", ">"]:
            self.read(self.current_token.value, "<OPERATOR>")
            self.A()
            self.buildTree("gr", 2)
        # Bp -> A ('ge' | '>=') A => 'ge'
        elif self.current_token.value in ["ge", ">="]:
            self.read(self.current_token.value, "<OPERATOR>")
            self.A()
            self.buildTree("ge", 2)
        # Bp -> A ('ls' | '<' ) A => 'ls'
        elif self.current_token.value in ["ls", "<"]:
            self.read(self.current_token.value, "<OPERATOR>")
            self.A()
            self.buildTree("ls", 2)
        # Bp -> A ('le' | '<=') A => 'le'
        elif self.current_token.value in ["le", "<="]:
            self.read(self.current_token.value, "<OPERATOR>")
            self.A()
            self.buildTree("le", 2)
        # Bp -> A 'eq' A => 'eq'
        elif self.current_token.value == "eq":
            self.read(self.current_token.value, "<OPERATOR>")
            self.A()
            self.buildTree("eq", 2)
        # Bp -> A 'ne' A => 'ne'
        elif self.current_token.value == "ne":
            self.read(self.current_token.value, "<OPERATOR>")
            self.A()
            self.buildTree("ne", 2)


    def A(self):
        # A -> '+' At
        if self.current_token.value == "+":
            self.read("+", "<OPERATOR>")
            self.At()
        # A -> '-' At => 'neg'
        elif self.current_token.value == "-":
            self.read("-", "<OPERATOR>")
            self.At()
            self.buildTree("neg", 1)
        else:
            self.At()  # A -> At
            while self.current_token.value in ["+", "-"]:
                # A ->A'+' At => '+'
                if self.current_token.value == "+":
                    self.read("+", "<OPERATOR>")
                    self.At()
                    self.buildTree("+", 2)
                # A -> A '-' At => '-'
                elif self.current_token.value == "-":
                    self.read("-", "<OPERATOR>")
                    self.At()
                    self.buildTree("-", 2)

    def At(self):
        self.Af()  # A -> Af
        while self.current_token.value in ["*", "/"]:
            # At -> At '*' Af => '*'
            if self.current_token.value == "*":
                self.read("*", "<OPERATOR>")
                self.Af()
                self.buildTree("*", 2)
            # At -> At '/' Af => '/'
            elif self.current_token.value == "/":
                self.read("/", "<OPERATOR>")
                self.Af()
                self.buildTree("/", 2)

    def Af(self):
        self.Ap()  # Af -> Ap
        # Af -> Ap '**' Af => '**'
        if self.current_token.value == "**":
            self.read("**", "<OPERATOR>")
            self.Af()
            self.buildTree("**", 2)


    def Ap(self):
        self.R()  # Ap -> R
        # Ap -> Ap '@' '<IDENTIFIER>' R => '@'
        while self.current_token.value == "@":
            self.read("@", "<OPERATOR>")
            self.read("UserDefined", "<IDENTIFIER>")
            self.buildTree("<ID:" + self.prevToken.value + ">", 0)
            self.R()
            # self.buildTree("@", 2)
            self.buildTree("@", 3)

    # Check this function
    def R(self):
        self.Rn()  # R -> Rn
        # R ->R Rn => 'gamma'
        while self.current_token.type in [
            "<IDENTIFIER>",
            "<INTEGER>",
            "<STRING>",
        ] or self.current_token.value in [
            "true",
            "false",
            "nil",
            "(",
            "dummy",
        ]:
            self.Rn()
            self.buildTree("gamma", 2)

    def Rn(self):
        # Rn -> '<IDENTIFIER>'
        if self.current_token.type == "<IDENTIFIER>":
            self.read("UserDefined", "<IDENTIFIER>")
            self.buildTree("<ID:" + self.prevToken.value + ">", 0)

        # Rn -> '<INTEGER>'
        elif self.current_token.type == "<INTEGER>":
            self.read("UserDefined", "<INTEGER>")
            self.buildTree("<INT:" + self.prevToken.value + ">", 0)
        # Rn -> '<STRING>'
        elif self.current_token.type == "<STRING>":
            self.read("UserDefined", "<STRING>")
            self.buildTree("<STR:" + self.prevToken.value + ">", 0)
        # Rn -> 'true' => 'true'
        elif self.current_token.value == "true":
            self.read("true", "<KEYWORD>")
            self.buildTree("true", 0)
        # Rn -> 'false' => 'false'
        elif self.current_token.value == "false":
            self.read("false", "<KEYWORD>")
            self.buildTree("false", 0)
        # Rn -> 'nil' => 'nil'
        elif self.current_token.value == "nil":
            self.read("nil", "<KEYWORD>")
            self.buildTree("nil", 0)
        # Rn -> '(' E ')'
        elif self.current_token.value == "(":
            self.read("(", "(")
            self.E()
            if self.current_token.value != ")":
                print("Error: expected )")
                self.errorExist = True
                return
            self.read(")", ")")
        # Rn -> 'dummy' => 'dummy'
        elif self.current_token.value == "dummy":
            self.read("dummy", "<KEYWORD>")
            self.buildTree("dummy", 0)

    def D(self):
        self.Da()  # D -> Da
        # D -> Da 'within' D => 'within'
        while self.current_token.value == "within":
            self.read("within", "<KEYWORD>")
            self.D()
            self.buildTree("within", 2)

    def Da(self):
        self.Dr()  # Da -> Dr
        n = 0  # keep track of repitation of Dr
        # Da -> Dr ( 'and' Dr )+ => 'and'
        while self.current_token.value == "and":
            self.read("and", "<KEYWORD>")
            self.Dr()
            n += 1
        if n > 0:
            self.buildTree("and", n + 1)

    def Dr(self):
        # Dr -> 'rec' Db => 'rec'
        if self.current_token.value == "rec":
            self.read("rec", "<KEYWORD>")
            self.Db()
            self.buildTree("rec", 1)
        else:
            # Dr -> Db
            self.Db()

    
    def Db(self):
        # Db -> '(' D ')'
        if self.current_token.value == "(":
            self.read("(", "(")
            self.D()
            if self.current_token.value != ")":
                print("Error: expected )")
                self.errorExist = True
                return
            self.read(")", ")")
        n = 0
        if self.current_token.type == "<IDENTIFIER>":
            # Db -> Vl '=' E => '='
            self.Vl()

            if self.current_token.value == "=":
                self.read("=", "<OPERATOR>")
                self.E()
                self.buildTree("=", 2)
            else:
                # Db-> '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
                self.Vb()
                n = 1
                while self.current_token.type in ["<IDENTIFIER>", "("]:
                    self.Vb()
                    n += 1
                if self.current_token.value != "=":
                    print("Error: expected in")
                    self.errorExist = True
                    return
                self.read("=", "<OPERATOR>")
                self.E()
                self.buildTree("fcn_form", n + 2)


    def Vb(self):
        # Vb -> '<IDENTIFIER>'
        if self.current_token.type == "<IDENTIFIER>":
            self.read("UserDefined", "<IDENTIFIER>")
            self.buildTree("<ID:" + self.prevToken.value + ">", 0)

        elif self.current_token.value == "(":
            self.read("(", "(")
            # Vb -> '(' Vl ')'
            if self.current_token.type == "<IDENTIFIER>":
                self.Vl()
                if self.current_token.value != ")":
                    print("Error: expected in")
                    self.errorExist = True
                    return
                self.read(")", ")")
            # Vb -> '(' ')'
            else:
                if self.current_token.value != ")":
                    print("Error: expected in")
                    self.errorExist = True
                    return
                self.read(")", ")")
                self.buildTree("()", 0)


    def Vl(self):
        # Vl -> '<IDENTIFIER>' list ',' => ','?
        if self.current_token.type == "<IDENTIFIER>":
            self.read("UserDefined", "<IDENTIFIER>")
            self.buildTree("<ID:" + self.prevToken.value + ">", 0)

            n = 0
            while self.current_token.value == ",":
                self.read(",", ",")
                self.read("UserDefined", "<IDENTIFIER>")
                self.buildTree("<ID:" + self.prevToken.value + ">", 0)
                n += 1
            if n > 0:
                self.buildTree(",", n + 1)
        

scanner = RPAL_Scanner("tests/div")     #Give the name of the file 
tokens = scanner.Scanning()
myParser = ASTParser(tokens)
myParser.startParsing()

print("Last index of the read input =", myParser.index)
