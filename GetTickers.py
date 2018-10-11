import re


class GetTickers:
    def __init__(self, filename):
        with open(filename) as NYSE:
            self.str_temp= NYSE.read()
            self.expression = re.compile("([A-Z]{1,5})\n+")
            self.arr_temp = self.expression.findall(self.str_temp)

    def g(self):
        return self.arr_temp


