from num import NUM
from sym import SYM

class COLS:
    def __init__(self, row):
        self.x = {}  # Independent variables
        self.y = {}  # Dependent variables
        self.all = []  # All columns
        self.klass = None  # Class column
        self.names = row.cells  # Column names

        for at, txt in enumerate(row.cells):
            # Choose column type based on case; NUM for uppercase, else SYM
            col_type = NUM if txt.isupper() else SYM
            col = col_type(txt, at)
            self.all.append(col)

            # Skip variables ending in 'X'
            if not txt.endswith("X"):
                # Class columns end in '!'
                if txt.endswith("!"):
                    self.klass = col
                # Add to `y` if ending in '!', '+', or '-', else add to `x`
                if any(txt.endswith(suffix) for suffix in ["!", "+", "-"]):
                    self.y[at] = col
                else:
                    self.x[at] = col

    def add(self, row):
        # Update columns with new row data
        for cols in (self.x, self.y):
            for col in cols.values():
                col.add(row.cells[col.at])
        return row
