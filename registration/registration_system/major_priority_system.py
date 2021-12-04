from typing import Dict, List, Tuple
import random
random.seed(100)

from registration.registration_system.lottery_system import LotterySystem
from registration.course import Course
from registration.student import Student


class MajorPrioritySystem(LotterySystem):
    def __init__(self, courses_dict: Dict[str, Course]) -> None:
        """class for Lottery System

        Args:
            courses_dict (Dict[str, Course]): whole courses for this registration
        """
        super().__init__(courses_dict)

    def register_students(self, students: List[Student], p: Tuple) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register
            p (Tuple): the probabilities to give priority for major students

        Returns:
            List[Student]: registered students
        """
        assert len(p) == 3, "Length of p should be 3"

        major_probability, double_major_probability, minor_probability = p
        assert major_probability + double_major_probability + minor_probability < 1, "Sum of three values should be less than 1"
        assert 0 < major_probability < 1, "Major probability must be a value between 0 and 1"
        assert 0 < double_major_probability < 1, "Double major probability must be a value between 0 and 1"
        assert 0 < minor_probability < 1, "Minor probability must be a value between 0 and 1"
        
        self.set_registration_list(students)

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
                major_students = {"major": [], "double_major": [], "minor": [], "remaining": []}
                for student in register_list:
                    if student.major == course.major:
                        major_students["major"].append(student)
                    elif student.double_major == course.major:
                        major_students["double_major"].append(student)
                    elif student.minor == course.major:
                        major_students["minor"].append(student)
                    else:
                        major_students["remaining"].append(student)

                major_priority_capacity = min(int(course.capacity * major_probability), len(major_students["major"]))
                double_major_priority_capacity = min(int(course.capacity * double_major_probability), len(major_students["double_major"]))
                minor_priority_capacity = min(int(course.capacity * minor_probability), len(major_students["minor"]))
                remaining_capacity = course.capacity - major_priority_capacity - double_major_priority_capacity - minor_priority_capacity

                # Randomly select students ordered by priority
                remained_students = []
                random.shuffle(major_students["major"])
                for i, student in enumerate(major_students["major"]):
                    if i < major_priority_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                major_students["double_major"].extend(remained_students)
                remained_students = []
                random.shuffle(major_students["double_major"])
                for i, student in enumerate(major_students["double_major"]):
                    if i < double_major_priority_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                major_students["minor"].extend(remained_students)
                remained_students = []
                random.shuffle(major_students["minor"])
                for i, student in enumerate(major_students["minor"]):
                    if i < minor_priority_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                major_students["remaining"].extend(remained_students)
                random.shuffle(major_students["remaining"])
                for i, student in enumerate(major_students["remaining"]):
                    if i < remaining_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        break

        return students