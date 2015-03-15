class Expense(object):
    def __init__(self):
        self.megacredits = 0
        self.supplies = 0
        self.neutronium = 0
        self.duranium = 0
        self.tritanium = 0
        self.molybdenum = 0

    def add(self, expense):
        e = Expense() 
        e.megacredits = self.megacredits+expense.megacredits
        e.supplies = self.supplies+expense.supplies
        e.neutronium = self.neutronium+expense.neutronium
        e.duranium = self.duranium+expense.duranium
        e.tritanium = self.tritanium+expense.tritanium
        e.molybdenum = self.molybdenum+expense.molybdenum
        return e


class Megacredits(Expense):
    def __init__(self, amount):
        super(Megacredits, self).__init__()
        self.megacredits = amount

class Supplies(Expense):
    def __init__(self, amount):
        super(Supplies, self).__init__()
        self.supplies = amount

class Neutronium(Expense):
    def __init__(self, amount):
        super(Neutronium, self).__init__()
        self.neutronium = amount

class Duranium(Expense):
    def __init__(self, amount):
        super(Duranium, self).__init__()
        self.duranium = amount

class Tritanium(Expense):
    def __init__(self, amount):
        super(Tritanium, self).__init__()
        self.tritanium = amount

class Molybdenum(Expense):
    def __init__(self, amount):
        super(Molybdenum, self).__init__()
        self.molybdenum = amount
