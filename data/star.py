from spacetrack import SpaceTrackClient
from models.Satellite import Satellite
from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
import numpy as np
from sgp4.api import WGS72, Satrec
from sgp4.exporter import export_tle
from astropy.time import Time
satellite = []


def get_data():
    st = SpaceTrackClient("hipeoplea@yandex.ru", "mx8-zHj-fiY-EdT")
    resp = st.tle_latest(ordinal=1, format='tle').split('\n')
    with open("data\\newData.txt", 'w') as f:
        f.writelines(resp)


def getSats():
    with open("data\data.txt") as f:
        fil = f.readlines()
    satellite.clear()
    for line in range(0, len(fil), 2):
        try:
            firstLine, secondLine = fil[line].strip(), fil[line + 1].strip()
            satellite.append(Satellite(firstLine, secondLine))
        except RuntimeError:
            continue
    print("successfully get satellites")


def fromRVtoTLE(id, r, v, epoch):
    orbit = Orbit.from_vectors(Earth, r, v, epoch)

    # Получение орбитальных элементов
    a = orbit.a.to(u.km).value  # Полу-мажорная ось в км
    print(a)
    ecc = orbit.ecc.value  # Эксцентриситет
    print(ecc)
    inc = orbit.inc.value    # Наклонение в градусах
    print(inc)
    raan = orbit.raan.value  # Долгота восходящего узла в градусах
    print(raan)
    argp = orbit.argp.value   # Аргумент перицентра в градусах
    print(argp)
    nu = orbit.n.value   # Истинная аномалия в градусах
    print(nu)

    # Расчет среднего движения (mean motion) в оборотах за день
    mean_motion = np.sqrt(Earth.k.to(u.km ** 3 / u.s ** 2).value / (a ** 3)) * (24 * 60 * 60)
    # Создание объекта Satrec и инициализация орбитальными элементами
    satellite = Satrec()
    satellite.sgp4init(
        WGS72,  # WGS84 гравитационная модель
        'i',  # 'i' для инициализации
        int(id),  # Номер спутника
        epoch.jd,  # Эпоха в формате Julian Date
        0.0, 0.0, 0.0,  # bstar, ndot, nddot
        ecc,  # Эксцентриситет
        argp,  # Аргумент перицентра в радианах
        inc,
          # Наклонение в радианах
        nu,  # Истинная аномалия в радианах
        mean_motion,
        raan,
        # Среднее движение (обороты в сутки)
         # Долгота восходящего узла в радианах
    )

    # Преобразование в TLE
    tle_line1, tle_line2 = export_tle(satellite)
    print(tle_line1)
    print(tle_line2)
    return Satellite(tle_line1, tle_line2)


# r = np.array([7000,  -12124, 0]) * u.km  # Вектор положения в км
# v = np.array([2.6679, 4.6210, 0]) * u.km / u.s  # Вектор скорости в км/с
# epoch = Time("2024-05-25 00:00:00", scale="utc")  # Время в формате UTC
# fromRVtoTLE(1212, r, v, epoch)
