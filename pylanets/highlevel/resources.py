class Expense():
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

    def sub(self, expense):
        e = Expense() 
        e.megacredits = self.megacredits-expense.megacredits
        e.supplies = self.supplies-expense.supplies
        e.neutronium = self.neutronium-expense.neutronium
        e.duranium = self.duranium-expense.duranium
        e.tritanium = self.tritanium-expense.tritanium
        e.molybdenum = self.molybdenum-expense.molybdenum
        return e

    def over(self):
        return self.megacredits < 0 or \
               self.supplies    < 0 or \
               self.neutronium  < 0 or \
               self.duranium    < 0 or \
               self.tritanium   < 0 or \
               self.molybdenum  < 0

    @property
    def deficient(self):
        """ return a list of what resources are < 0 or empty list if none """
        r = []
        if self.megacredits < 0:
            r.append('C')
        if self.supplies < 0:
            r.append('S')
        if self.neutronium < 0:
            r.append('N')
        if self.duranium < 0:
            r.append('D')
        if self.molybdenum < 0:
            r.append('M')
        return r

    def __repr__(self):
        return 'C{},S{},N{},D{},T{},M{}'.format(self.megacredits,
                                                self.supplies,
                                                self.neutronium,
                                                self.duranium,
                                                self.tritanium,
                                                self.molybdenum)


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

C = Megacredits
N = Neutronium
D = Duranium
T = Tritanium
M = Molybdenum
