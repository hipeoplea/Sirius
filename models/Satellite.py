import datetime

from models.tle import Tle
from models.state import State
from astropy.time import Time
from models.KeplerianElements import KeplerianElements
from datetime import datetime
from sgp4.api import jday, Satrec
from astropy import units as u
from astropy.coordinates import CartesianRepresentation, CartesianDifferential
from poliastro.bodies import Earth
from poliastro.twobody import Orbit


class Satellite:
    def __init__(self, line1, line2):
        self.__tle = Tle(line1, line2)
        self.__id = self.__tle.get_id()
        date = self.__getDate()
        sat = Satrec.twoline2rv(line1, line2)
        kep = self.__getKep(date[0], date[1], sat)
        self.__state = kep[0]
        self.__kep = kep[1]
        self.__realDate = [self.__tle.get_epochYear(), self.__tle.get_epochTime()]
        self.__exchangedDate = date

    def __getDate(self):
        now = datetime.utcnow()

        # Преобразование текущего времени в компоненты года, месяца, дня, часа, минуты и секунды
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second + now.microsecond / 1e6

        # Получение юлианской даты с использованием функции jday из библиотеки sgp4
        jd, fr = jday(year, month, day, hour, minute, second)

        return [jd, fr]

    def __getKep(self, jd, fr, satellite):
        e, r, v = satellite.sgp4(jd, fr)
        if e != 0:
            raise RuntimeError(f'Error computing satellite position and velocity: error code {e}')
        state = State(r, v, jd)

        r = r * u.km
        v = v * u.km / u.s

        orbit = Orbit.from_vectors(Earth, r, v)

        kep = KeplerianElements(orbit.a, orbit.ecc, orbit.inc, orbit.raan, orbit.argp, orbit.nu)
        return [state, kep]

    def __str__(self):
        kep = self.__kep
        state = self.__state

        return (f"Satellite ID: {self.__id}\n"
                f"Real Date: Year {self.__realDate[0]}, Day {self.__realDate[1]}\n"
                f"Exchanged Date (Julian): {self.__exchangedDate[0]} + {self.__exchangedDate[1]}\n"
                f"State Vector:\n"
                f"  Position (km): {state.get_r()}\n"
                f"  Velocity (km/s): {state.get_v()}\n"
                f"Keplerian Elements:\n"
                f"  Semi-major axis (a): {kep.a}\n"
                f"  Eccentricity (e): {kep.ecc}\n"
                f"  Inclination (i): {kep.inc.to(u.deg)}\n"
                f"  RA of ascending node (Ω): {kep.raan.to(u.deg)}\n"
                f"  Argument of perigee (ω): {kep.argp.to(u.deg)}\n"
                f"  True anomaly (ν): {kep.nu.to(u.deg)}")
