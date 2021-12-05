from enum import Enum

class SystemType(str, Enum):
    LOTTERY = "Lottery"
    MAJOR_PRIORITY = "Major Priority"
    GRADE_PRIORITY = "Grade Priority"
    TOP3_PRIORITY = "Top3 Priority"
    TOP3_BASED1 = "Top3-Based 1"
    TOP3_BASED2 = "Top3-Based 2"
