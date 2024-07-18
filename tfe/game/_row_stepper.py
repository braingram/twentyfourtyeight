
class Row:
    def __init__(self, row):
        self.values = row
    
    @property
    def empty(self):
        return sum(self.values) == 0

    def _shift(self):
        i = 0
        while sum(self.values[i:]) != 0 and i < 3:
            if self.values[i] == 0:
                self.values.pop(i)
                self.values.append(0)
            else:
                i += 1

    def _combine(self):
        left_combined = False
        for i in range(3):
            v = self.values[i]
            if v == 0:
                break
            r = self.values[i + 1]
            if v != r:
                continue
            self.values[i] *= 2
            self.values.pop(i+1)
            self.values.append(0)


    def step(self):
        # simple edge case
        if self.empty:
            return self.values
        self._shift()
        self._combine()
        return self.values


def step_row(row):
    return Row(row).step()
