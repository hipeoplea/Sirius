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
        return self.rx,self.ry,self.rz

    def get_v(self):
        return self.vx,self.vy,self.vz
