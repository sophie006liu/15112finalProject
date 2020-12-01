import math

class Fraction(object):
    def __init__(self, top=0, bot=1):
        self.top = int(top)
        self.bot = int(bot)

    def add(self, frac2):
        bot = self.bot
        self.bot *= frac2.bot
        self.top *= frac2.bot
        self.top += frac2.top * bot
        self.simplify()
        return self


    def sub(self, frac2):
        bot = self.bot
        self.bot *= frac2.bot
        self.top *= frac2.bot
        self.top -= frac2.top * bot
        self.simplify()
        return self

    def mul(self, frac2):
        self.bot *= frac2.bot
        self.top *= frac2.top
        self.simplify()
        return self

    def inv(self):
        temp = self.top
        self.top = self.bot
        self.bot = temp
        return self

    def div(self, frac2):
        self.bot *= frac2.top
        self.top *= frac2.bot
        return self

    def scale(self, s):
        self.top *= s
        return self


# helper functions

    def simplify(self):
        temp = math.gcd(self.bot, self.top)
        self.bot  = int(self.bot / temp)
        self.top  = int(self.top / temp)

    def print_frac(self):
        print(str(self.top) + "/" + str(self.bot))

    def from_float(f):
        bot = 1000000000
        top = int(f * bot)
        frac = Fraction(top, bot)
        frac.simplify()
        return frac

    def to_float(self):
        return float(self.top)/float(self.bot)

    def cp(self):
        return Fraction(self.top, self.bot)

    def min(self, frac2):
        if self.top * frac2.bot < self.bot*frac2.top:
            return self
        else:
            return frac2

    def max(self, frac2):
        if self.top * frac2.bot < self.bot*frac2.top:
            return frac2
        else:
            return self  


## another set of methods return new object

    def add2(self, frac2):
        prev_bot = self.bot
        bot = self.bot * frac2.bot
        top = self.top * frac2.bot
        top += frac2.top * prev_bot
        frac = Fraction(top, bot)
        frac.simplify()
        return frac

    def sub2(self, frac2):
        bot = self.bot * frac2.bot
        top = self.top * frac2.bot
        top = top - frac2.top * self.bot
        frac = Fraction(top, bot)
        frac.simplify()
        return frac

    def mul2(self, frac2):
        bot = self.bot * frac2.bot
        top = self.top * frac2.top
        frac = Fraction(top, bot)
        frac.simplify()
        return frac

    def div2(self, frac2):
        bot = self.bot * frac2.top
        top = self.top * frac2.bot
        return Fraction(top, bot)
    
    def scale2(self, s):
        top = self.top * s
        return Fraction(top, self.bot)

#also starts the simulation
def main():
    f1 = Fraction(1,2)
    f2 = Fraction(2,3)
    f1.add(f2)
    f1.print_frac()

    f1 = Fraction(1,2)
    f1.sub(f2)
    f1.print_frac()
    
    f1 = Fraction(1,2)
    f1.mul(f2)
    f1.print_frac()

    f1 = Fraction(1,2)
    f1.div(f2)
    f1.print_frac()
    
    f1 = Fraction(1,2)
    f1.inv()
    f1.print_frac()

    f1 = Fraction.from_float(0.125)
    f1.print_frac()

    f1 = Fraction(1,2)
    f3 = f1.add2(f2)
    f3.print_frac()

    f1 = Fraction(1,2)
    f3 = f1.sub2(f2)
    f3.print_frac()
    
    f1 = Fraction(1,2)
    f3 = f1.mul2(f2)
    f3.print_frac()

    f1 = Fraction(1,2)
    f3 = f1.div2(f2)
    f3.print_frac()
    
    f4 = Fraction.from_float(0.2)
    f4.print_frac()
    f5 = f1.mul2(f4)
    f5.print_frac()

    f1 = Fraction(1,2)
    f2 = Fraction(2,3)
    f = f1.min(f2)
    f.print_frac()

    f = f1.max(f2)
    f.print_frac()
if __name__ == '__main__':
    main()