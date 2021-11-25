from enum import Enum
from typing import Dict, List, Tuple
import numpy as np
import random
random.seed(100)

from registration.course import Course
from registration.major import Major
from registration.student import Student


class SystemType(Enum):
    LOTTERY = 1
    MAJOR_PRIORITY = 2
    GRADE_PRIORITY = 3
    TOP3_PRIORITY = 4


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

        major_percentage, double_major_percentage, minor_percentage = p
        assert major_percentage + double_major_percentage + minor_percentage < 1, "Sum of three values should be less than 1"

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

                major_priority_capacity = int(course.capacity * major_percentage)
                double_major_priority_capacity = int(course.capacity * double_major_percentage)
                minor_priority_capacity = int(course.capacity * minor_percentage)

                registered_students_count = 0
                random.shuffle(major_students["major"])
                for i, student in enumerate(major_students["major"]):
                    if i < major_priority_capacity:
                        student.add_to_final_timetable(course)
                        registered_students_count += 1
                    else:
                        break

                random.shuffle(major_students["double_major"])
                for i, student in enumerate(major_students["double_major"]):
                    if i < double_major_priority_capacity:
                        student.add_to_final_timetable(course)
                        registered_students_count += 1
                    else:
                        break

                random.shuffle(major_students["minor"])
                for i, student in enumerate(major_students["minor"]):
                    if i < minor_priority_capacity:
                        student.add_to_final_timetable(course)
                        registered_students_count += 1
                    else:
                        break

                remaining = major_students["remaining"]
                if major_priority_capacity < len(major_students["major"]):
                    remaining += major_students["major"][major_priority_capacity:]
                if double_major_priority_capacity < len(major_students["double_major"]):
                    remaining += major_students["double_major"][double_major_priority_capacity:]
                if minor_priority_capacity < len(major_students["minor"]):
                    remaining += major_students["minor"][minor_priority_capacity:]

                random.shuffle(remaining)
                for i, student in enumerate(remaining):
                    if i < (course.capacity - registered_students_count):
                        student.add_to_final_timetable(course)
                    else:
                        break

        return students

      
class GradePrioritySystem(LotterySystem):
    def __init__(self, courses_dict: Dict[str, Course]) -> None:
        """class for Grade Priority System

        Args:
            courses_dict (Dict[str, Course]): whole courses for this registration
        """
        super().__init__(courses_dict)

    def register_students(self, students: List[Student], graduate_standard: int, percentage: int) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register
            graduate_standard (int): year to regard as graduate-to-be
            percentage (float): the probability to give priority for graduate-to-be students

        Returns:
            List[Student]: registered students
        """
        assert percentage < 1

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

                grade_priority_capacity = int(course.capacity * percentage)

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


class Top3PrioritySystem(LotterySystem):
    def __init__(self, courses: Dict[str, Course]) -> None:
        super().__init__(courses)

    def designate_priority(self, students: List[Student], p: Tuple) -> List[Student]:
        """Designate students' class priority

        Args:
            students (List[Student]): students to register
            p (Tuple): the probabilities of choosing a highly competitive major class, liberal art class, and other class as the priority

        Returns:
            List[Student]: prioritized students
        """
        assert len(p) == 3, "Length of p should be 3"
        
        p1, p2, p3 = p
        assert p1 + p2 + p3 == 1, "Sum of three values should be 1"

        # Reorder students' timetable order to consider priority
        for student in students:
            is_major = []
            is_liberal_art = []
            competition_rate = []
            course_len = len(student.timetable)

            for course in student.timetable:
                is_major.append(course.major == student.major)
                is_liberal_art.append(course.major == Major.HSS)
                competition_rate.append(0 if course.capacity==0 else course.get_num_applicants()/course.capacity)

            is_major = np.array(is_major).astype(np.bool)
            is_liberal_art = np.array(is_liberal_art).astype(np.bool)
            is_other = ~is_major & ~is_liberal_art
            competition_rate = np.array(competition_rate)
            new_order = np.arange(course_len)

            prioritys = random.choices([1, 2, 3], [p1, p2, p3], k=3)

            def switch_courses(i: int, priority: int) -> List[List]:
                list_to_check = {1: is_major, 2: is_liberal_art, 3: is_other}[priority]
                
                # If there's no course, skip
                if len(list_to_check[i:]) == 0:
                    return

                # If there's no course that satisfies the condition, random select
                if list_to_check[i:].any() == False:
                    random_idx = random.randint(i, course_len-1)
                    is_major[[i, random_idx]] = is_major[[random_idx, i]]
                    is_liberal_art[[i, random_idx]] = is_liberal_art[[random_idx, i]]
                    competition_rate[[i, random_idx]] = competition_rate[[random_idx, i]]
                    new_order[[i, random_idx]] = new_order[[random_idx, i]]
                    return

                max_idx = np.argmax(competition_rate[i:][list_to_check[i:] == True])
                switch_idx = np.where(list_to_check[i:] == True)[0][max_idx] + i # [0] for removing tuple type
                is_major[[i, switch_idx]] = is_major[[switch_idx, i]]
                is_liberal_art[[i, switch_idx]] = is_liberal_art[[switch_idx, i]]
                competition_rate[[i, switch_idx]] = competition_rate[[switch_idx, i]]
                new_order[[i, switch_idx]] = new_order[[switch_idx, i]]

            for i, priority in enumerate(prioritys):
                switch_courses(i, priority)

            new_timetable = [student.timetable[i] for i in new_order]
            student.timetable = new_timetable

        return students
                

    def register_students(self, students: List[Student], p: Tuple) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register
            p (Tuple): the probabilities of assigning first, second, and third-prioritized students

        Returns:
            List[Student]: registered students
        """
        assert len(p) == 3, "Length of p should be 3"

        p1, p2, p3 = p
        assert p1 + p2 + p3 < 1, "Sum of three values should be less than 1"

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
                top3_prioritized = {"first": [], "second": [], "third": [], "etc": []}

                for student in register_list:
                    for priority, student_course in enumerate(student.timetable):
                        if student_course.code == code:
                            if priority == 0:
                                top3_prioritized["first"].append(student)
                            elif priority == 1:
                                top3_prioritized["second"].append(student)
                            elif priority == 2:
                                top3_prioritized["third"].append(student)
                            else:
                                top3_prioritized["etc"].append(student)
                            
                            continue

                first_capacity = min(int(course.capacity * p1), len(top3_prioritized["first"]))
                second_capacity = min(int(course.capacity * p2), len(top3_prioritized["second"]))
                third_capacity = min(int(course.capacity * p3), len(top3_prioritized["third"]))
                fourth_capacity = course.capacity - first_capacity - second_capacity - third_capacity

                # Randomly select students ordered by priority
                remained_students = []
                random.shuffle(top3_prioritized["first"])
                for i, student in enumerate(top3_prioritized["first"]):
                    if i < first_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                top3_prioritized["second"].extend(remained_students)
                remained_students = []
                random.shuffle(top3_prioritized["second"])
                for i, student in enumerate(top3_prioritized["second"]):
                    if i < second_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                top3_prioritized["third"].extend(remained_students)
                remained_students = []
                random.shuffle(top3_prioritized["third"])
                for i, student in enumerate(top3_prioritized["third"]):
                    if i < third_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                top3_prioritized["etc"].extend(remained_students)
                random.shuffle(top3_prioritized["etc"])
                for i, student in enumerate(top3_prioritized["etc"]):
                    if i < fourth_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        break

        return students
