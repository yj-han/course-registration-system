import sys
[sys.path.append(i) for i in ['.', '..']]

import unittest
import pprint
import copy

from registration.course import Course
from registration.major import Major
from registration.registration_system import PrioritizeSystem
from registration.student import Degree, Student

class TestRegistrationSystem(unittest.TestCase):
    def test_lottery_system(self):
        # Course 1: does not need lottery
        course1 = Course(
            "Intro to Computer Science",
            "CS101",
            Major.CS,
            3,
            3,
            None,
            3,
            False,
            False
        )
        # Course 2: no limit
        course2 = Course(
            "Programming Principles",
            "CS220",
            Major.CS,
            3,
            0,
            None,
            5,
            False,
            False
        )
        # Course 3: needs lottery - Major
        course3 = Course(
            "System Programming",
            "CS230",
            Major.CS,
            3,
            3,
            None,
            5,
            True,
            False
        )
        # Course 4: needs lottery - Liberal Art
        course4 = Course(
            "Spanish Conversation",
            "HSS179",
            Major.HSS,
            3,
            3,
            None,
            5,
            True,
            False
        )
        # Course 5: needs lottery - Other
        course5 = Course(
            "Basics of Artificial Intelligence<Physical AI>",
            "CoE202",
            Major.CoE,
            3,
            3,
            None,
            5,
            True,
            False
        )

        courses_dict = {
            course1.code: course1, 
            course2.code: course2, 
            course3.code: course3, 
            course4.code: course4, 
            course5.code: course5
        }
        
        student1 = Student("A", 
                    2020, 
                    Degree.BACHELOR, 
                    Major.CS,
                    None, 
                    [course1, course2, course3, course4, course5],
                    [])
        student2 = Student("D", 
                    2020, 
                    Degree.BACHELOR, 
                    Major.CS,
                    None, 
                    [course2, course3, course4, course5],
                    [])
        students = [student1, copy.deepcopy(student1), copy.deepcopy(student1),\
                    student2, copy.deepcopy(student2)]

        # run the test
        prioritize_system = PrioritizeSystem(courses_dict)
        prioritized_students = prioritize_system.designate_priority(copy.deepcopy(students), (0.5, 0.4, 0.1))
        results = prioritize_system.register_students(copy.deepcopy(prioritized_students), (0.2, 0.2, 0.2))

        if print_result:
            pprint.pprint(students)
            print()
            pprint.pprint(prioritized_students)
            print()
            pprint.pprint(results)
                    
        for course in [course1]:
            self.assertEqual(course.num_applicants, 3)
        for course in [course2, course3, course4, course5]:
            self.assertEqual(course.num_applicants, 5)

        applicants_dict = {course1:0, course2:0, course3:0, course4:0, course5:0}

        for student in results:
            for course in student.final_timetable:
                applicants_dict[course] += 1

        for course in [course2]: # no limit case
            self.assertEqual(applicants_dict[course], 5)
        for course in [course1, course3, course4, course5]:
            self.assertEqual(applicants_dict[course], 3)
    
if __name__ == "__main__":
    # Change to see the result
    print_result = False
    
    unittest.main()