from typing import Dict, List, Tuple
import numpy as np
import random
random.seed(100)

from registration.registration_system.lottery_system import LotterySystem
from registration.course import Course
from registration.major import Major
from registration.student import Student


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
        
        major_probability, liberal_art_probability, other_probability = p
        assert major_probability + liberal_art_probability + other_probability == 1, "Sum of three values should be 1"
        assert 0 < major_probability < 1, "Major probability must be a value between 0 and 1"
        assert 0 < liberal_art_probability < 1, "Liberal art probability must be a value between 0 and 1"
        assert 0 < other_probability < 1, "Other probability must be a value between 0 and 1"
        
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

            is_major = np.array(is_major)
            is_liberal_art = np.array(is_liberal_art)
            is_other = ~is_major & ~is_liberal_art
            competition_rate = np.array(competition_rate)
            new_order = np.arange(course_len)

            prioritys = random.choices([1, 2, 3], [major_probability, liberal_art_probability, other_probability], k=3)

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

        first_probability, second_probability, third_probability = p
        assert first_probability + second_probability + third_probability < 1, "Sum of three values should be less than 1"
        assert 0 < first_probability < 1, "First probability must be a value between 0 and 1"
        assert 0 < second_probability < 1, "Second probability must be a value between 0 and 1"
        assert 0 < third_probability < 1, "Third probability must be a value between 0 and 1"

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

                first_capacity = min(int(course.capacity * first_probability), len(top3_prioritized["first"]))
                second_capacity = min(int(course.capacity * second_probability), len(top3_prioritized["second"]))
                third_capacity = min(int(course.capacity * third_probability), len(top3_prioritized["third"]))
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