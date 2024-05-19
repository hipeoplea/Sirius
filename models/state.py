class State:
    def __init__(self, r, v, jd):
        self.rx = r[0]
        self.ry = r[1]
        self.rz = r[2]
        self.vx = v[0]
        self.vy = v[1]
        self.vz = v[2]
        self.jd = jd

    def get_r(self):
        return str(self.rx) + " " + str(self.ry) + " " + str(self.rz)

    def get_v(self):
        return str(self.vx) + " " + str(self.vy) + " " + str(self.vz)