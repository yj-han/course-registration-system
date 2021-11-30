from enum import Enum

class MARKER(str, Enum):
    LOTTERY = "H"
    MAJOR = None
    GRADE = None
    TOP3 = None
    TOP3B1 = "x"
    ELSE = "^"

    @classmethod
    def value_of(cls, value):
        if value == "lottery":
            return cls.LOTTERY
        elif value == "major priority":
            return cls.MAJOR
        elif value == "grade priority":
            return cls.GRADE
        elif value == "top3 priority":
            return cls.TOP3
        elif value == "top3 based 1":
            return cls.TOP3B1
        else:
            return cls.ELSE