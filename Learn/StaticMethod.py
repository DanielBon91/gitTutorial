# class StaticTest:
#    x = 1
#
# t1 = StaticTest()
#
# print('instance', t1.x)
# print('class', StaticTest.x)
#
# t1.x = 2
#
# print('instance', t1.x)
# print('class', StaticTest.x)
#
# StaticTest.x = 3
#
# print('instance', t1.x)
# print('class', StaticTest.x)
################################

class Date:

    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

    def display(self):
        return f"{self.day}-{self.month}-{self.year}"

    @classmethod
    def millenium_c(cls, day, month):
        return cls(day, month, 2000)

    @staticmethod
    def millenium_s(day, month):
        return Date(day, month, 2000)

class DateTime(Date):
    def display(self):
        return f"{self.month}-{self.day}-{self.year} - 00:00:00PM"


dt1 = DateTime(10, 10, 1990)
dt2 = DateTime.millenium_s(10, 10)

print(isinstance(dt1, DateTime))#True
print(isinstance(dt2, DateTime))#False
print(dt1.display())            #10-10-1990 - 00:00:00PM
print(dt2.display())            #10-10-2000



