from collections import defaultdict

from calculation.constants import *
from calculation.checkSats import *
from data.star import get_data, getSats, satellite
from ui import main
from models.Satellite import Satellite
import socket
from apscheduler.schedulers.background import BackgroundScheduler


# def a(sat: List[Satellite]):
#     answ = defaultdict(list)
#     k = 1
#     for i in sat:
#         for j in sat[k:]:
#             if i.get_id() == j.get_id():
#                 continue
#             if i.get_kep().r_a.value - j.get_kep().r_p.value < 100:
#                 answ[i.get_id()].append(j.get_id())
#         k += 1
#     return answ



if __name__ == "__main__":
    getSats()
    main()



