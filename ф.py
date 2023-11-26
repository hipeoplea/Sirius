class Car():
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.rast = 0

    def drive(self, t):
        self.rast += t * self.speed
        return self.rast

def chto_to(to_to=None):
    return to_to

print(chto_to(6))

print('Drive')

a = Car('маша', 100)
b = Car('злата', 80)
c = Car('яна', 80)

print(a.name, a.drive(5))
print(b.name, b.drive(3))
print(c.name, c.drive(10))