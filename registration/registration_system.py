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
        registration_dict = {
            k: {
                "course": v, 
                "register_list": []
            } for k, v in self.courses_dict.items()
        }
        self.registration_dict = registration_dict
        
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
                self.registration_dict[course.code]["register_list"].append(student)

        # Randomly select students from each course
        for code, register_info in self.registration_dict.items():
            course = register_info["course"]
            register_list = register_info["register_list"]
            
            self.courses_dict[code].num_applicants = len(register_list)

            if not course.is_lottery:
                for student in register_list:
                    student.add_to_final_timetable(course)
                continue
            else:
                random.shuffle(register_list)
                for i, student in enumerate(register_list):
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
        