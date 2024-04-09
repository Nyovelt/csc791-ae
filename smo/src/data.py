from cols import COLS
from row import ROW
import l 
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
import llm
class DATA:
    def __init__(self, src=None, fun=None):
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            # Assuming l.csv is a method to parse CSV files
            for x in l.csv(src):
                self.add(x, fun)
        else:
            for x in (src or []):
                self.add(x, fun)    

    def add(self, t, fun=None):
        row = t if hasattr(t, 'cells') else ROW(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)
    def print(self):
        print(self.cols)
        for row in self.rows:
            row.print()

    def mid(self, cols=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW(u)

    def div(self, cols=None):
        u = [col.div() for col in (cols or self.cols.all)]
        return ROW(u)

    def small(self):
        u = [col.small() for col in self.cols.all]
        return ROW(u)

    def stats(self, cols=None, fun=None, ndivs=None):
        u = {".N": len(self.rows)}
        target_cols = self.cols[cols or "y"]
        for col in target_cols.values():
            col_function = getattr(col, fun or "mid")
            u[col.txt] = l.rnd(col_function(), ndivs)
        return u


    def gate(self, budget0, budget, some):
        stats, bests = {}, {}
        rows = l.shuffle(self.rows)  
        # Print baseline1 and baseline2
        print("1. top6", [round(row.d2h(self),2) for row in rows[:6]])  
        print("2. top50", [round(row.d2h(self),2)  for row in rows[:50]])
        lite, dark = rows[:budget0], rows[budget0:]
        best, rest = self.bestRest(lite, len(lite) ** some)
        print("3. most", round(best.rows[0].d2h(self), 2))
        for i in range(1, budget + 1):
            best, rest = self.bestRest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)
            print("4. rand", round(dark[todo].d2h(self),2))
            stats[i] = selected.mid()
            bests[i] = best.rows[0]
            lite.append(dark.pop(todo))
            print("5. selected", round(stats[i].d2h(self), 2))
            print("6. best", round(bests[i].d2h(self),2))
        return stats, bests


    # def gate(self, budget0, budget, some):
    #     stats, bests = {}, {}
    #     rows = l.shuffle(self.rows)  
    #     # Print baseline1 and baseline2
    #     print("1. top6", [row.cells for row in rows[:6]])  
    #     print("2. top50", [row.cells for row in rows[:50]])
    #     lite, dark = rows[:budget0], rows[budget0:]
    #     for i in range(1, budget + 1):
    #         best, rest = self.bestRest(lite, len(lite) ** some)
    #         todo, selected = self.split(best, rest, lite, dark)
    #         stats[i] = selected.mid()
    #         bests[i] = best.rows[0]
    #         lite.append(dark.pop(todo))
    #     return stats, bests

    def split(self, best, rest, lite, dark):
        selected = DATA([self.cols.names])
        max_score = float('inf')
        output_row_index = 1

        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            if b > r:
                selected.add(row)
            
            tmp = abs(b + r) / abs(b - r + 1e-300)
            if tmp < max_score:
                output_row_index, max_score = i, tmp
        
        return output_row_index, selected


    def bestRest(self, rows, want):
        # Sort rows based on distance to heaven
        rows.sort(key=lambda row: row.d2h(self))
        
        # Sort rows based on LLM
        rows = llm.sort_rows_with_preference(rows, "more reliable")
        
        # Initialize 'best' and 'rest' with column names
        best = [self.cols.names]
        rest = [self.cols.names]

        # Split rows into 'best' and 'rest'
        for i, row in enumerate(rows):
            if i < want:
                best.append(row)
            else:
                rest.append(row)

        # Return new DATA objects created from 'best' and 'rest'
        return DATA(best), DATA(rest)


