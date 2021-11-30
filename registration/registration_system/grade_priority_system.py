from typing import Dict, List
import random
random.seed(100)

from registration.registration_system.lottery_system import LotterySystem
from registration.course import Course
from registration.student import Student


class GradePrioritySystem(LotterySystem):
    def __init__(self, courses_dict: Dict[str, Course]) -> None:
        """class for Grade Priority System

        Args:
            courses_dict (Dict[str, Course]): whole courses for this registration
        """
        super().__init__(courses_dict)

    def register_students(self, students: List[Student], graduate_standard: int, probability: int) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register
            graduate_standard (int): year to regard as graduate-to-be
            probability (float): the probability to give priority for graduate-to-be students

        Returns:
            List[Student]: registered students
        """
        assert probability < 1

        self.set_registration_list(students)

        for code, register_info in self.registration_dict.items():
            course = register_info["course"]
            register_list = register_info["register_list"]

            self.courses_dict[code].num_applicants = len(register_list)

            if not course.is_lottery:
                for student in register_list:
                    student.add_to_final_timetable(course)
                continue
            else:
                grade_dict = {"candidates": [], "remaining": []}
                for student in register_list:
                    if student.year <= graduate_standard:
                        grade_dict["candidates"].append(student)
                    else:
                        grade_dict["remaining"].append(student)

                grade_priority_capacity = int(course.capacity * probability)

                random.shuffle(grade_dict["candidates"])
                for i, student in enumerate(grade_dict["candidates"]):
                    if i < grade_priority_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        break

                remaining = grade_dict["remaining"]
                if grade_priority_capacity < len(grade_dict["candidates"]):
                    remaining += grade_dict["candidates"][grade_priority_capacity:]

                random.shuffle(remaining)
                for i, student in enumerate(remaining):
                    if i < (course.capacity - grade_priority_capacity):
                        student.add_to_final_timetable(course)
                    else:
                        break

        return students