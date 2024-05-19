class Tle:
    def __init__(self, line1, line2):
        self.__numberOfLine1 = line1[0:1]
        self.__satelliteNumbers1 = line1[2:7]
        self.__classification = line1[7:8]
        self.__internationalDesignatorYear = line1[9:11]
        self.__internationalDesignator = line1[11:14]
        self.__piece = line1[14:17]
        self.__epochYear = line1[18:20]
        self.__epochTime = line1[20:32]
        self.__meanMotionDerivative = line1[33:43]
        self.__meanMotionSecondDerivative = line1[44:52]
        self.__averageAcceleration = line1[53:61]
        self.__typeOfEphemeris = line1[62:63]
        self.__elementsNumber = line1[64:68]
        self.__chkSum = line1[68]

        self.__numberOfLine2 = line2[0:1]
        self.__satelliteNumbers2 = line2[2:7]
        self.__inclination = line2[8:16]
        self.__rightAscensionOfTheNode = line2[17:25]
        self.__eccentricity = line2[26:33]
        self.__argOfPerigee = line2[34:42]
        self.__meanAnomaly = line2[43:51]
        self.__meanMotion = line2[52:63]
        self.__epochRev = line2[63:68]
        self.__chk = line2[68]
        self.__id = int(self.get_satelliteNumbers1().replace(" ", ""))

    def get_numberOfLine1(self):
        return self.__numberOfLine1

    def get_satelliteNumbers1(self):
        return self.__satelliteNumbers1

    def get_classification(self):
        return self.__classification

    def get_internationalDesignatorYear(self):
        return self.__internationalDesignatorYear

    def get_internationalDesignator(self):
        return self.__internationalDesignator

    def get_piece(self):
        return self.__piece

    def get_epochYear(self):
        return self.__epochYear

    def get_epochTime(self):
        return self.__epochTime

    def get_meanMotionDerivative(self):
        return self.__meanMotionDerivative

    def get_meanMotionSecondDerivative(self):
        return self.__meanMotionSecondDerivative

    def get_averageAcceleration(self):
        return self.__averageAcceleration

    def get_typeOfEphemeris(self):
        return self.__typeOfEphemeris

    def get_elementsNumber(self):
        return self.__elementsNumber

    def get_chkSum(self):
        return self.__chkSum

    def get_numberOfLine2(self):
        return self.__numberOfLine2

    def get_satelliteNumbers2(self):
        return self.__satelliteNumbers2

    def get_inclination(self):
        return self.__inclination

    def get_rightAscensionOfTheNode(self):
        return self.__rightAscensionOfTheNode

    def get_eccentricity(self):
        return self.__eccentricity

    def get_argOfPerigee(self):
        return self.__argOfPerigee

    def get_meanAnomaly(self):
        return self.__meanAnomaly

    def get_meanMotion(self):
        return self.__meanMotion

    def get_epochRev(self):
        return self.__epochRev

    def get_chk(self):
        return self.__chk

    def get_id(self):
        return self.__id

