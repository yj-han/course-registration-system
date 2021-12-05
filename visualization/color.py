from enum import Enum
from registration.registration_system.system_type import SystemType


class COLOR(str, Enum):
    LOTTERY = "#1f77b4"
    MAJOR_PRIORITY = "#ff7f0e"
    GRADE_PRIORITY = "#2ca02c"
    TOP3_PRIORITY = "d62728"
    TOP3_BASED1 = "#9467bd"
    TOP3_BASED2 = "#8c564b"
    ELSE = "#e377c2"

    @classmethod
    def value_of(cls, value):
        if value == SystemType.LOTTERY:
            return cls.LOTTERY
        elif value == SystemType.MAJOR_PRIORITY:
            return cls.MAJOR_PRIORITY
        elif value == SystemType.GRADE_PRIORITY:
            return cls.GRADE_PRIORITY
        elif value == SystemType.TOP3_PRIORITY:
            return cls.TOP3_PRIORITY
        elif value == SystemType.TOP3_BASED1:
            return cls.TOP3_BASED1
        elif value == SystemType.TOP3_BASED2:
            return cls.TOP3_BASED2        
        else:
            return cls.ELSE