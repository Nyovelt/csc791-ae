class NODE:
    def __init__(self, data):
        self.here = data
        self.lefts = None
        self.rights = None

    def walk(self, fun, depth=0):
        # Apply the function to the current node
        fun(self, depth, not (self.lefts or self.rights))
        # Recursively apply to left and right subtrees if they exist
        if self.lefts:
            self.lefts.walk(fun, depth + 1)
        if self.rights:
            self.rights.walk(fun, depth + 1)

    def show(self, maxDepth=0):
        def _show(node, depth, leafp):
            # Assuming `d2h` and `l.o` equivalents in Python
            post = (d2h(node.here) + "\t" + str(node.here.mid().cells)) if leafp else ""
            nonlocal maxDepth
            maxDepth = max(maxDepth, depth)
            print(('|.. ' * depth) + post)

        def d2h(data):
            # Placeholder for `d2h` calculation, assuming an equivalent rounding function
            return round(data.mid().d2h(self.here), 2)

        self.walk(_show)
        print("\n" + "    " * maxDepth, d2h(self.here), str(self.here.mid().cells))
        print("    " * maxDepth, "_", str(self.here.cols.names))

