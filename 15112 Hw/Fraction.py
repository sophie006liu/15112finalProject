import math

class Fraction(object):

    def init(self, top=0, bot=1):
        self.top = top
        self.bot = bot

    def add(self, frac2):
        self.bot *= frac2.bot
        self.top *= frac2.bot
        self.top += frac2.top * self.bot
        self.simplify()

    def simplify(self):
        temp = math.gcd(self.bot, self.top)
        self.bot /= temp
        self.top /= temp

    def subtract(self, frac2):
        self.bot *= frac2.bot
        self.top *= frac2.bot
        self.top -= frac2.top * self.bot
        self.simplify()

    def multiply(self, frac2):
        self.bot *= frac2.bot
        self.top *= frac2.top
        self.simplify()

    def invert(self, frac2):
        temp = self.top
        self.top = self.bot
        self.bot = temp

    def divide(self, frac2):
        self.bot *= frac2.top
        self.top *= frac2.bot

    def print_frac(self):
        print(str(self.top) + "/" + str(self.bot))

    def equals(self, frac2):
        self.simplify()
        frac2.simplify()
        return ((self.top == frac2.top) and (self.bot == frac2.bot))