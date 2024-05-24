from typing import List
from scipy.integrate import solve_ivp
from calculation.constants import mu3
import numpy as np
import math

from models.Satellite import Satellite


def selection(x: Satellite, n: List[Satellite]):
    answer = []
    k = 0
    for i in n:
        if i.get_id() == x.get_id():
            continue
        if i.get_kep().r_a.value - x.get_kep().r_p.value < 100:
            k += 1
            n = secondStep(i, x)
            p = integrate(x, i)
            if p != 0:
                answer.append([p[0], p[1].get_id()])
    print(k)
    return answer


def secondStep(i, j):
    n = find_u(i, j)
    answer = []
    if n == 0:
        return 0
    if abs(n[0] - n[1]) < 200:
        answer.append([n[0], n[1]])
    if abs(n[2] - n[3]) < 200:
        answer.append([n[2], n[3]])
    if len(answer) > 0:
        return answer
    return 0


def find_u(sat1: Satellite, sat2: Satellite):
    i_ka = sat1.get_kep().inc.value
    i_ko = sat2.get_kep().inc.value
    delta_omega = sat1.get_kep().raan.value - sat2.get_kep().raan.value
    gamma = math.acos(-math.cos(i_ko) * math.cos(i_ka) + math.sin(i_ko) * math.sin(i_ka) * math.cos(delta_omega))
    opposite = math.pi - gamma
    ap1 = sat1.get_kep().argp.value
    ap2 = sat2.get_kep().argp.value
    a1 = sat1.get_kep().a.value
    a2 = sat2.get_kep().a.value
    points = []
    if gamma > 5:
        p = get_points(i_ka, i_ko, gamma, ap1, ap2, a1, a2)
        for n in p:
            points.append(n)
    if opposite > 5:
        p = get_points(i_ka, i_ko, opposite, ap1, ap2, a1, a2)
        for n in p:
            points.append(n)
    if points:
        return points
    return 0


def get_points(i_ka, i_ko, gamma, ap1, ap2, a1, a2):
    try:
        b = math.asin(math.sin(gamma) * math.sin(i_ka) / math.sin(i_ko))
        c = math.asin(math.sin(gamma) * math.sin(i_ko) / math.sin(i_ka))
        cos_u0 = (math.cos(b) - math.cos(c) * math.cos(gamma)) / (math.sin(c) * math.sin(gamma))
        cos_u1 = (math.cos(c) - math.cos(b) * math.cos(gamma)) / (math.sin(b) * math.sin(gamma))
        answer = []
        v0 = math.acos(cos_u0) - ap1
        p0 = a1
        answer.append(p0 / (1 + math.cos(v0)))
        v1 = math.acos(cos_u1) - ap2
        p1 = a2
        answer.append(p1 / (1 + math.cos(v1)))
        return answer
    except ValueError:
        return []


def integrate(x: Satellite, y: Satellite, p=None):
    t_span = (0, 3600)
    time_step = 20
    t_eval = np.arange(0, 3600, time_step)
    initial_state1 = np.hstack((x.get_state().get_r(), x.get_state().get_v()))
    initial_state2 = np.hstack((y.get_state().get_r(), y.get_state().get_v()))
    solution1 = solve_ivp(orbital_dynamics, t_span, initial_state1, t_eval=t_eval, method='RK45')
    solution2 = solve_ivp(orbital_dynamics, t_span, initial_state2, t_eval=t_eval, method='RK45')
    positions1 = solution1.y[:3].T
    positions2 = solution2.y[:3].T
    for i in range(180):
        r1r2 = math.sqrt((positions1[i][0] - positions2[i][0]) ** 2 + (positions1[i][1] - positions2[i][1]) ** 2 + (
                    positions1[i][2] - positions2[i][2]) ** 2)
        if r1r2 < 100:
#51178
            return [r1r2, y]

    return 0

def orbital_dynamics(t, y):
    r = np.linalg.norm(y[:3])
    ax = -mu3 * y[0] / r ** 3
    ay = -mu3 * y[1] / r ** 3
    az = -mu3 * y[2] / r ** 3
    return [y[3], y[4], y[5], ax, ay, az]
