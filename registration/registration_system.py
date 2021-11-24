from enum import Enum
from typing import Dict, List, Tuple
import numpy as np
import random
random.seed(100)

from registration.course import Course
from registration.major import Major
from registration.student import Student


class SystemType(Enum):
    FCFS = 1;
    LOTTERY = 2;
    PRIORITIZE = 3;
    BETTING = 4;
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
    
class PrioritizeSystem(LotterySystem):
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
        assert p1+p2+p3 == 1, "Sum of three values should be 1"

        # Reorder students' timetable order to consider priority
        for student in students:
            is_major = []
            is_liberal_art = []
            competition_rate = []
            course_len = len(student.timetable)

            for course in student.timetable:
                is_major.append(course.major == student.major)
                is_liberal_art.append(course.major == Major.HSS)
                competition_rate.append(0 if course.capacity==0 else course.num_applicants/course.capacity)

            is_major = np.array(is_major)
            is_liberal_art = np.array(is_liberal_art)
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
        assert p1+p2+p3 < 1, "Sum of three values should be less than 1"

        # Create a registration list for each course
        for student in students:
            for course in student.timetable:
                self.registration_dict[course.code]["register_list"].append(student)

        # Randomly select students from each course considering priority
        for code, register_info in self.registration_dict.items():
            course = register_info["course"]
            register_list = register_info["register_list"]
            
            self.courses_dict[code].num_applicants = len(register_list)

            if not course.is_lottery:
                for student in register_list:
                    student.add_to_final_timetable(course)
                continue
            else:
                # Make priority list considering the order of students' timetable
                first_prioritized = []
                second_prioritized = []
                third_prioritized = []
                fourth_prioritized = []

                for student in register_list:
                    for priority, student_course in enumerate(student.timetable):
                        if student_course.code == code:
                            if priority == 0:
                                first_prioritized.append(student)
                            elif priority == 1:
                                second_prioritized.append(student)
                            elif priority == 2:
                                third_prioritized.append(student)
                            else:
                                fourth_prioritized.append(student)
                            
                            continue

                first_capacity = min(int(course.capacity * p1), len(first_prioritized))
                second_capacity = min(int(course.capacity * p2), len(second_prioritized))
                third_capacity = min(int(course.capacity * p3), len(third_prioritized))
                fourth_capacity = course.capacity - first_capacity - second_capacity - third_capacity

                # Randomly select students ordered by priority
                remained_students = []
                random.shuffle(first_prioritized)
                for i, student in enumerate(first_prioritized):
                    if i < first_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                second_prioritized.extend(remained_students)
                remained_students = []
                random.shuffle(second_prioritized)
                for i, student in enumerate(second_prioritized):
                    if i < second_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                third_prioritized.extend(remained_students)
                remained_students = []
                random.shuffle(third_prioritized)
                for i, student in enumerate(third_prioritized):
                    if i < third_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        remained_students.append(student)

                fourth_prioritized.extend(remained_students)
                random.shuffle(fourth_prioritized)
                for i, student in enumerate(fourth_prioritized):
                    if i < fourth_capacity:
                        student.add_to_final_timetable(course)
                    else:
                        break

        return students
    
    def register_students_with_restraints(self, students: List[Student]) -> List[Student]:
        return students


class MajorPrioritySystem(RegistrationSystem):
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

    def register_students(self, students: List[Student], major_percentage: int, double_major_percentage: int, minor_percentage: int) -> List[Student]:
        """Register students to courses

        Args:
            students (List[Student]): students to register
            percentage (int): percentage to give priority for major students

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

            if len(register_list) <= course.capacity or not course.is_lottery:
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

                random.shuffle(major_students["major"])
                major_priority_capacity = int(course.capacity * major_percentage / 100)
                double_major_priority_capacity = int(course.capacity * double_major_percentage / 100)
                minor_priority_capacity = int(course.capacity * minor_percentage / 100)

                registered_students_count = 0
                for i, student in enumerate(major_students["major"]):
                    if i < major_priority_capacity:
                        student.add_to_final_timetable(course)
                        registered_students_count += 1
                    else:
                        break

                for i, student in enumerate(major_students["double_major"]):
                    if i < double_major_priority_capacity:
                        student.add_to_final_timetable(course)
                        registered_students_count += 1
                    else:
                        break

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
                    remaining += major_students["doble_major"][double_major_priority_capacity:]
                if minor_priority_capacity < len(major_students["minor"]):
                    remaining += major_students["minor"][minor_priority_capacity:]

                random.shuffle(remaining)
                for i, student in enumerate(remaining):
                    if i < (course.capacity - registered_students_count):
                        student.add_to_final_timetable(course)
                    else:
                        break

        return students

    def register_students_with_restraints(self, students: List[Student]) -> List[Student]:
        return students