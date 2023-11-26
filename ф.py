class Car():
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.rast = 0

    def drive(self, t):
        self.rast += t * self.speed
        return self.rast


a = Car('маша', 100)
b = Car('злата', 80)
c = Car('яна', 80)

print(a.name, a.drive(5))
print(b.name, b.drive(3))
print(c.name, c.drive(10))


