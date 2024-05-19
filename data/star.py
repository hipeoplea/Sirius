from spacetrack import SpaceTrackClient
from models.Satellite import Satellite


def get_data():
    st = SpaceTrackClient("hipeoplea@yandex.ru", "mx8-zHj-fiY-EdT")
    resp = st.tle_latest(ordinal=1, format='tle').split('\n')
    with open("data\\newData.txt", 'w') as f:
        f.writelines(resp)


def getSats():
    sats = []
    with open("data\data.txt") as f:
        fil = f.readlines()
    for line in range(0, len(fil), 2):
        try:
            firstLine, secondLine = fil[line].strip(), fil[line + 1].strip()
            sats.append(Satellite(firstLine, secondLine))

        except RuntimeError:
            continue
    print("successfully get satellites")
    return sats

get_data()
satellites = getSats()
print(satellites[0])
