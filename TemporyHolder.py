    def buildTree(self, token, ariness):
        global stack

        print("stack content before ")
        for node in stack:
            print(node.type)

        print("building tree")

        node = ASTNode(token)
        node.value = None
        node.sourceLineNumber = -1
        node.child = None
        node.sibling = None

        while ariness > 0:
            # print("error in while loop")
            child = stack[-1]
            stack.pop()
            # Assuming pop() is a function that returns an ASTNode
            if node.child is not None:
                child.sibling = node.child
            node.child = child
            node.sourceLineNumber = child.sourceLineNumber
            ariness -= 1
            # print("test")
        # print("root", node.type)
        node.print_tree()

        stack.append(
            node
        )  # Assuming push() is a function that pushes a node onto a stack
        print("stack content after")
        for node in stack:
            print(node.type)

    # Parsing table
    def E(self):
        print("E")
        match self.current_token.value:

            case "let":
                self.read()
                self.D()

                if self.current_token.value != "in":
                    print("Error: in is expected")
                    return

                self.read()
                self.E()
                print("E->let D in E")
                self.buildTree("let", 2)

            case "fn":

                n = 0

                self.read()

                while (
                    self.current_token.type == Tokernizer.TokenType.ID
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

                self.read()
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
            self.read()
            self.Dr()
            print("Ew->T where Dr")
            self.buildTree("where", 2)

    def T(self):
        print("T")
        self.Ta()
        # print('T->Ta')

        n = 0
        while self.current_token.value == ",":
            self.read()
            self.Ta()
            n += 1
            print("T->Ta , Ta")
        if n > 0:
            self.buildTree("tau", n + 1)
        else:
            print("T->Ta")

    def Ta(self):
        print("Ta")
        self.Tc()
        print("Ta->Tc")
        while self.current_token.value == "aug":
            self.read()
            self.Tc()
            print("Ta->Tc aug Tc")

            self.buildTree("aug", 2)

    def Tc(self):
        print("Tc")

        self.B()
        print("Tc->B")
        if self.current_token.type == Tokernizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.Tc()

            if self.current_token.value != "|":
                print("Error: | is expected")
                return
            self.read()
            self.Tc()
            print("Tc->B -> Tc | Tc")
            self.buildTree("->", 3)

    def B(self):
        print("B")

        self.Bt()
        print("B->Bt")
        while self.current_token.value == "or":
            self.read()
            self.Bt()
            print("B->B or B")
            self.buildTree("or", 2)

    def Bt(self):
        print("Bt")

        self.Bs()
        print("Bt->Bs")
        while self.current_token.value == "&":
            self.read()
            self.Bs()
            print("Bt->Bs & Bs")
            self.buildTree("&", 2)

    def Bs(self):
        print("Bs")

        if self.current_token.value == "not":
            self.read()
            self.Bp()
            print("Bs->not Bp")
            self.buildTree("not", 1)
        else:
            self.Bp()
            print("Bs->Bp")

    def Bp(self):
        print("Bp")

        self.A()
        print("Bp->A")
        print(self.current_token.value + "######")

        ##  Bp -> A ( 'gr' | '>') A
        match self.current_token.value:
            case ">":
                self.read()
                self.A()
                print("Bp->A gr A")
                self.buildTree("gr", 2)
            case "gr":
                self.read()
                self.A()
                print("Bp->A gr A")
                self.buildTree("gr", 2)

            case "ge":
                self.read()
                self.A()
                print("Bp->A ge A")
                self.buildTree("ge", 2)

            case ">=":
                self.read()
                self.A()
                print("Bp->A ge A")
                self.buildTree("ge", 2)

            case "<":
                self.read()
                self.A()
                print("Bp->A ls A")
                self.buildTree("ls", 2)

            case "ls":
                self.read()
                self.A()
                print("Bp->A ls A")
                self.buildTree("ls", 2)

            case "<=":
                self.read()
                self.A()
                print("Bp->A le A")
                self.buildTree("le", 2)

            case "le":
                self.read()
                self.A()
                print("Bp->A le A")
                self.buildTree("le", 2)

            case "eq":
                self.read()
                self.A()
                print("Bp->A eq A")
                self.buildTree("eq", 2)

            case "ne":
                self.read()
                self.A()
                print("Bp->A ne A")
                self.buildTree("ne", 2)

            case _:
                return

    def A(self):
        print("A")

        if self.current_token.value == "+":
            self.read()
            self.At()
            print("A->+ At")
            # self.buildTree("+", 1)

        elif self.current_token.value == "-":
            self.read()
            self.At()
            print("A->- At")
            self.buildTree("neg", 1)

        else:
            self.At()
            print("A->At")
        plus = "+"
        while self.current_token.value == "+" or self.current_token.value == "-":

            if self.current_token.value == "-":
                plus = "-"

            self.read()
            self.At()
            print("A->A + / -At")
            print(self.current_token.value)
            self.buildTree(plus, 2)

    def At(self):
        print("At")

        self.Af()
        print("At->Af")
        while self.current_token.value == "*" or self.current_token.value == "/":
            self.read()
            self.Af()
            print("At->Af * Af")
            print("current token value " + self.current_token.value)
            self.buildTree(self.current_token.value, 2)

    def Af(self):
        print("Af")

        self.Ap()
        print("Af->Ap")
        while self.current_token.value == "**":
            self.read()
            self.Af()
            print("Af->Ap ** Af")
            self.buildTree("**", 2)

    def Ap(self):
        print("Ap")

        self.R()
        print("Ap->R")
        while self.current_token.value == "@":
            self.read()
            self.R()
            print("Ap->R @ R")
            self.buildTree("@", 2)

    def R(self):
        print("R")

        self.Rn()
        print("R->Rn")
        # self.read()

        while self.current_token.type in [
            Tokernizer.TokenType.ID,
            Tokernizer.TokenType.INT,
            Tokernizer.TokenType.STRING,
        ] or self.current_token.value in ["true", "false", "nil", "dummy", "("]:
            self.Rn()
            print("R->R Rn")
            self.buildTree("gamma", 2)

            # self.read()

    def Rn(self):
        print("Rn")

        if self.current_token.type in [
            Tokernizer.TokenType.ID,
            Tokernizer.TokenType.INT,
            Tokernizer.TokenType.STRING,
        ]:

            print("Rn->" + str(self.current_token.value))

            self.read()

            # self.read()
            # self.buildTree("id", 0)
        elif self.current_token.value in ["true", "false", "nil", "dummy"]:
            print("Rn->" + self.current_token.value)
            self.read()
            print("self.current_token.value", self.current_token.value)
            # self.buildTree(self.current_token.value, 0)
        elif self.current_token.value == "(":
            self.read()
            self.E()
            if self.current_token.value != ")":
                print("Error: ) is expected")
                return
            self.read()
            print("Rn->( E )")
            # self.buildTree("()", 1)

    def D(self):
        print("D")

        self.Da()
        print("D->Da")
        while self.current_token.value == "within":
            self.read()
            self.D()
            print("D->Da within D")
            self.buildTree("within", 2)

    def Da(self):
        print("Da")

        self.Dr()
        print("Da->Dr")
        n = 0
        while self.current_token.value == "and":
            n += 1
            self.read()
            self.Da()
            print("Da->and Dr")
        # if n == 0:
        #     print("Error")
        #     return
        if n > 0:
            self.buildTree("and", n + 1)

    def Dr(self):
        print("Dr")

        if self.current_token.value == "rec":
            self.read()
            self.Db()
            print("Dr->rec Db")
            self.buildTree("rec", 1)

        self.Db()
        print("Dr->Db")

    def Db(self):
        print("Db")

        if self.current_token.value == "(":
            self.read()
            self.D()
            if self.current_token.value != ")":
                print("Error: ) is expected")
                return
            self.read()
            print("Db->( D )")
            self.buildTree("()", 1)

        elif self.current_token.type == Tokernizer.TokenType.ID:
            self.read()

            if self.current_token.type == Tokernizer.TokenType.COMMA:
                # Db -> Vl '=' E => '='
                self.read()
                self.Vb()

                if self.current_token.value != "=":
                    print("Error: = is expected")
                    return
                self.buildTree(",", 2)
                self.read()
                self.E()
                self.buildTree("=", 2)
            else:
                if self.current_token.value == "=":
                    self.read()
                    self.E()
                    print("Db->id = E")
                    self.buildTree("=", 2)

                else:

                    n = 0
                    while (
                        self.current_token.type == Tokernizer.TokenType.ID
                        or self.current_token.value == "("
                    ):
                        self.Vb()
                        n += 1

                    if n == 0:
                        print("Error: ID or ( is expected")
                        return

                    if self.current_token.value != "=":
                        print("Error: = is expected")
                        return
                    self.read()
                    self.E()
                    print("Db->identifier Vb+ = E")
                    self.buildTree("function_form", n + 2)

        # else:
        #     self.VL()
        #     print(self.current_token.value)
        #     if self.current_token.value != '=':
        #         print("Error: = is expected")
        #         return
        #     self.read()
        #     self.E()
        #     print('Db->Vl = E')
        #     self.buildTree("=", 2)

    def Vb(self):
        print("Vb")
        if self.current_token.type == Tokernizer.TokenType.ID:
            self.read()
            print("Vb->id")
            # self.buildTree("id", 1)

        elif self.current_token.value == "(":
            self.read()
            # print(self.current_token.value)
            if self.current_token.type == ")":
                print("Vb->( )")
                self.buildTree("()", 0)
                self.read()
            else:
                self.VL()
                print("Vb->( Vl )")
                if self.current_token.value != ")":
                    print("Error: ) is expected")
                    return
            self.read()

            # self.buildTree("()", 1)

        else:
            print("Error: ID or ( is expected")
            return

    def VL(self):
        print("VL")
        print("559 " + str(self.current_token.value))

        if self.current_token.type != Tokernizer.TokenType.ID:
            print(
                "562 VL: Identifier expected"
            )  # Replace with appropriate error handling
        else:
            print("VL->" + self.current_token.value)

            self.read()
            trees_to_pop = 0
            while self.current_token.value == ",":
                # Vl -> '<IDENTIFIER>' list ',' => ','?;
                self.read()
                if self.current_token.type != Tokernizer.TokenType.ID:
                    print(
                        " 572 VL: Identifier expected"
                    )  # Replace with appropriate error handling
                self.read()
                print("VL->id , ?")

                trees_to_pop += 1
            print("498")
            if trees_to_pop > 0:
                self.buildTree(",", trees_to_pop + 1)  # +1 for the first identifier
