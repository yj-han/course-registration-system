from enum import Enum

class COLOR(str, Enum):
    LOTTERY = "r"
    MAJOR = "g"
    GRADE = "b"
    TOP3 = "c"
    ELSE = "k"
    
    @classmethod
    def value_of(cls, value):
        if "lottery" in value:
            return cls.LOTTERY
        elif "major" in value:
            return cls.MAJOR
        elif "grade" in value:
            return cls.GRADE
        elif "top3" in value:
            return cls.TOP3
        else:
            return cls.ELSE