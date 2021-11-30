from typing import Dict, List, Tuple
import numpy as np
import random
random.seed(100)

from registration.registration_system.top3_priority_system import Top3PrioritySystem
from registration.course import Course
from registration.major import Major
from registration.student import Student


class Top3Based1System(Top3PrioritySystem):
    def __init__(self, courses: Dict[str, Course]) -> None:
        super().__init__(courses)

    def register_students(self, students: List[Student], p: Tuple, major_guarantee: float, grade_guarantee: float, graduate_standard: int) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register
            p (Tuple): the probabilities of assigning first, second, and third-prioritized students
            major_guarantee: the guaranteed probability for major students
            grade_guarantee: the guaranteed probability for graduate-to-be students
            graduate_standard (int): year to regard as graduate-to-be

        Returns:
            List[Student]: registered students
        """
        assert len(p) == 3, "Length of p should be 3"

        first_probability, second_probability, third_probability = p
        assert first_probability + second_probability + third_probability < 1, "Sum of three values should be less than 1"
        assert 0 < first_probability < 1, "First probability must be a value between 0 and 1"
        assert 0 < second_probability < 1, "Second probability must be a value between 0 and 1"
        assert 0 < third_probability < 1, "Third probability must be a value between 0 and 1"

        assert 0 < major_guarantee < 1, "Major garauteed probability must be a value between 0 and 1"
        assert 0 < grade_guarantee < 1, "Grade garauteed probability must be a value between 0 and 1"

        self.set_registration_list(students)

        # Randomly select students from each course considering priority
        for code, register_info in self.registration_dict.items():
            course = register_info["course"]
            register_list = register_info["register_list"]
            assert course.get_num_applicants() == len(register_list), "Number of applicants should be equal to number of students"
            
            if not course.is_lottery:
                for student in register_list:
                    student.add_to_final_timetable(course)
                continue
            else:
                # Make priority list considering the order of students' timetable
                top3_based_1 = {"first": [], "second": [], "third": [], "guarantee": [], "etc": []}

                for student in register_list:
                    for priority, student_course in enumerate(student.timetable):
                        if student_course.code == code:
                            if priority == 0:
                                top3_based_1["first"].append(student)
                            elif priority == 1:
                                top3_based_1["second"].append(student)
                            elif priority == 2:
                                top3_based_1["third"].append(student)
                            else:
                                top3_based_1["guarantee"].append(student)
                            
                            continue

                first_capacity = min(int(course.capacity * first_probability), len(top3_based_1["first"]))
                second_capacity = min(int(course.capacity * second_probability), len(top3_based_1["second"]))
                third_capacity = min(int(course.capacity * third_probability), len(top3_based_1["third"]))
                fourth_capacity = course.capacity - first_capacity - second_capacity - third_capacity

                major_guaranteed_capacity = int(course.capacity * major_guarantee)
                grade_guaranteed_capacity = int(course.capacity * grade_guarantee)
                major_headcount = 0
                grade_headcount = 0

                # Randomly select students ordered by priority
                remained_students = []
                random.shuffle(top3_based_1["first"])
                for i, student in enumerate(top3_based_1["first"]):
                    if i < first_capacity:
                        student.add_to_final_timetable(course)
                        
                        if student.major == course.major:
                            major_headcount += 1
                        if student.year <= graduate_standard:
                            grade_headcount += 1
                    else:
                        remained_students.append(student)

                top3_based_1["second"].extend(remained_students)
                remained_students = []
                random.shuffle(top3_based_1["second"])
                for i, student in enumerate(top3_based_1["second"]):
                    if i < second_capacity:
                        student.add_to_final_timetable(course)
                        
                        if student.major == course.major:
                            major_headcount += 1
                        if student.year <= graduate_standard:
                            grade_headcount += 1
                    else:
                        remained_students.append(student)

                top3_based_1["third"].extend(remained_students)
                remained_students = []
                random.shuffle(top3_based_1["third"])
                for i, student in enumerate(top3_based_1["third"]):
                    if i < third_capacity:
                        student.add_to_final_timetable(course)
                        
                        if student.major == course.major:
                            major_headcount += 1
                        if student.year <= graduate_standard:
                            grade_headcount += 1
                    else:
                        remained_students.append(student)

                top3_based_1["guarantee"].extend(remained_students)
                random.shuffle(top3_based_1["guarantee"])
                
                guarantee_benefitted = 0
                for student in top3_based_1["guarantee"]:
                    if guarantee_benefitted >= fourth_capacity:
                        break

                    is_major = student.major == course.major
                    is_grade = student.year <= graduate_standard
                    more_major = major_headcount < major_guaranteed_capacity
                    more_grade = grade_headcount < grade_guaranteed_capacity

                    if is_major and is_grade and (more_major or more_grade):
                        student.add_to_final_timetable(course)
                        major_headcount += 1
                        grade_headcount += 1
                        guarantee_benefitted += 1
                    elif is_major and more_major:
                        student.add_to_final_timetable(course)
                        major_headcount += 1
                        guarantee_benefitted += 1
                    elif is_grade and more_grade:
                        student.add_to_final_timetable(course)
                        grade_headcount += 1
                        guarantee_benefitted += 1
                    else:
                        top3_based_1["etc"].append(student)

                random.shuffle(top3_based_1["etc"])
                for i, student in enumerate(top3_based_1["etc"]):
                    if i < fourth_capacity - guarantee_benefitted:
                        student.add_to_final_timetable(course)
                    else:
                        break

        return students