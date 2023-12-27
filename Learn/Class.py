class Charakter():
    max_speed = 100
    dead_health = 0

    def __init__(self, race, damage=10, armor=20):
        self.race = race
        self.damage = damage
        self.armor = armor
        self.health = 100

    def hit(self, damage):
        self.health -= damage

    def is_dead(self):
        return self.health == Charakter.dead_health


##########################################################
ork = Charakter("Ork")
print(ork.health)
ork.hit(20)
print(ork.health)
print(ork.is_dead())
ork.hit(80)
print(ork.is_dead())
##########################################################
class House():
    def __init__(self, street, number):
        self.street = street
        self.number = number
        self.age = 10

    def build(self):
        print("House auf dem Straße " + self.street + " ,hat nummer "  + str(self.number) + " -ist gebaut worden")

    def age_house(self, year):
        self



House1 = House("Estaya", 83)
House2 = House("Kairbaeva", 96)

print(House2.age)
House1.build()

