from enum import Enum
from typing import List

from course import Course
from student import Student


class SystemType(Enum):
    FCFS = 1;
    LOTTERY = 2;    
    BETTING = 3;
    # TODO: 더 필요한 경우 enum 추가하기


class RegistrationSystem:
    def __init__(self, courses: List[Course]) -> None:
        """Abstract class for Registration System

        Args:
            courses (List[Course]): Whole courses for this registration
        """
        self.courses = courses
        
    def run(students: List[Student]) -> List[Student]:
        return students

    def run_with_restraints(students: List[Student]) -> List[Student]:
        return students


# TODO: 코드가 길어질 경우 다른 코드로 이동
class FCFSSystem(RegistrationSystem):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        # TODO: FCFS에 필요한 init 추가


class LotterySystem(RegistrationSystem):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        # TODO: Lottery에 필요한 init 추가
    
    def run(students: List[Student]) -> List[Student]:
        pass
    
    def run_with_restraints(students: List[Student]) -> List[Student]:
        return students    
    
    
class BettingSystem(RegistrationSystem):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        # TODO: BettingSystem에 필요한 init 추가
    
    def run(students: List[Student]) -> List[Student]:
        pass
    
    def run_with_restraints(students: List[Student]) -> List[Student]:
        return students
        