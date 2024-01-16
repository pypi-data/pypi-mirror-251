class Calculator:
    def __init__(self, a, b):
        print(f"Initializing received params {a}, {b} to object")
        self.a = a
        self.b = b

    def add(self):
        print(f"ADD params {self.a}, {self.b}")
        return self.a + self.b

    def multiply(self):
        print(f"MULTIPLE params {self.a}, {self.b}")
        return self.a * self.b


def entry_point():
    c1 = Calculator(3,4)
    return c1.add()

