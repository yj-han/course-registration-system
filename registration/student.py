from enum import Enum, unique
from typing import List, Optional

from course import Course

@unique
class Degree(Enum):
    BACHELOR = 1
    MASTER = 2
    DOCTOR = 3
    # TODO: 석박통합이 필요할지 데이터보고 확인
    MS_PHD_INTEGRATION = 4

@unique    
class Major(Enum):
    CS = 1
    BS = 2
    EE = 3
    # TODO: 과목코드의 앞 두 자리와 같으므로 파싱하여 자동으로 코드 생성한 뒤 옮겨 붙이기 (알파벳 순으로 변경)

class Student:
    
    def __init__(self, 
                 id: str, 
                 degree: Degree,
                 major: Major, 
                 minor: Optional[Major] = None, 
                 timetable: List[Course] = [], 
                 final_timetable: List[Course] = []) -> None:
        """Initialization

        Args:
            id (str): [description]
            degree (Degree): [description]
            major (Major): [description]
            minor (Optional[Major]): [description]
            timetable (List[Course]): [description]
            final_timetable (List[Course]): [description]
        """
        self.id = id;
        self.degree = degree;
        self.major = major;
        self.minor = minor;
        self.timetable = timetable;
        self.final_timetable = final_timetable;
