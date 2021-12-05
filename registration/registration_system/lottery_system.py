from enum import Enum
from typing import Dict, List
import random
random.seed(100)

from registration.course import Course
from registration.student import Student


class RegistrationSystem:
    def __init__(self, courses_dict: Dict[str, Course]) -> None:
        """Abstract class for Registration System

        Args:
            courses_dict (Dict[str, Course]): whole courses for this registration
        """
        self.courses_dict = courses_dict
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
        return students


class LotterySystem(RegistrationSystem):
    def __init__(self, courses_dict: Dict[str, Course]) -> None:
        """class for Lottery System

        Args:
            courses_dict (Dict[str, Course]): whole courses for this registration
        """
        super().__init__(courses_dict)

    def set_registration_list(self, students: List[Student]) -> None:
        """Set registration list

        Args:
            students (List[Student]): students to register
        """
        # Create a registration list for each course
        for student in students:
            for course in student.timetable:
                self.registration_dict[course.code]["register_list"].append(student)
        
    def register_students(self, students: List[Student]) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register

        Returns:
            List[Student]: registered students
        """
        self.set_registration_list(students)

        # Randomly select students from each course
        for code, register_info in self.registration_dict.items():
            course = register_info["course"]
            register_list = register_info["register_list"]
            assert course.get_num_applicants() == len(register_list), "Number of applicants should be equal to number of students"

            if not course.is_lottery:
                for student in register_list:
                    student.add_to_final_timetable(course)
                continue
            else:
                random.shuffle(register_list)
                for i, student in enumerate(register_list):
                    if course.capacity == 0 or i < course.capacity:
                        student.add_to_final_timetable(course)
                    else:
                        break
            
        return students