    void createControlStructures(tree *x, tree *(*setOfControlStruct)[200])
    {
        static int index = 1;
        static int j = 0;
        static int i = 0;
        static int betaCount = 1;
        if (x == NULL)
            return;
