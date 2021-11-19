from enum import Enum
from typing import Dict, List
import random
random.seed(100)

from registration.course import Course
from registration.student import Student


class SystemType(Enum):
    FCFS = 1;
    LOTTERY = 2;    
    BETTING = 3;
    # TODO: 더 필요한 경우 enum 추가하기


class RegistrationSystem:
    def __init__(self, courses_dict: Dict[str, Course]) -> None:
        """Abstract class for Registration System

        Args:
            courses_dict (Dict[str, Course]): whole courses for this registration
        """
        self.courses_dict = courses_dict
        
    def register_students(self, students: List[Student]) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register

        Returns:
            List[Student]: registered students
        """
        return students

    def register_students_with_restraints(self, students: List[Student]) -> List[Student]:
        return students


class LotterySystem(RegistrationSystem):
    def __init__(self, courses_dict: Dict[str, Course]) -> None:
        """class for Lottery System

        Args:
            courses_dict (Dict[str, Course]): whole courses for this registration
        """
        super().__init__(courses_dict)
        registered_students = dict.fromkeys(courses_dict.keys() , [])
        self.registered_students = registered_students
        
    def register_students(self, students: List[Student]) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register

        Returns:
            List[Student]: registered students
        """
        # Create a registration list for each course
        for student in students:
            for course in student.timetable:
                self.registered_students[course.code].append(student)
        
        # Randomly select students from each course
        for code, students in self.registered_students.items():
            self.courses_dict[code].num_applicants = len(students)
            
            if not course.is_lottery:
                map(lambda student: student.add_to_final_timetable(course), students)
                continue
            else:
                random.shuffle(students)
                for i, student in enumerate(students):
                    if i < course.capacity:
                        student.add_to_final_timetable(course)
                    else:
                        break
            
        return students
    
    def register_students_with_restraints(self, students: List[Student]) -> List[Student]:
        return students
    

# TODO: 코드가 길어질 경우 다른 코드로 이동
class FCFSSystem(RegistrationSystem):
    def __init__(self, courses: Dict[str, Course]) -> None:
        super().__init__(courses)
        # TODO: FCFS에 필요한 init 추가
    
class BettingSystem(RegistrationSystem):
    def __init__(self, courses: Dict[str, Course]) -> None:
        super().__init__(courses)
        # TODO: BettingSystem에 필요한 init 추가
    
    def register_students(self, students: List[Student]) -> List[Student]:
        pass
    
    def register_students_with_restraints(self, students: List[Student]) -> List[Student]:
        return students
        