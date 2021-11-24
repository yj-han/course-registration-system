import sys
[sys.path.append(i) for i in ['.', '..']]

import unittest
import pprint
import copy

from registration.course import Course, Semester
from registration.major import Major
from registration.registration_system import PrioritizeSystem
from registration.student import Degree, Student

# Change to see the result
PRINT_RESULT = False
class TestRegistrationSystem(unittest.TestCase):
    def test_lottery_system(self):
        semester = Semester.SPRING
        
        # Course 1: does not need lottery
        course1 = Course(
            "Intro to Computer Science",
            "CS101",
            Major.CS,
            3,
            None,
            False,
            semester,
            3,
            False
        )
        course1.set_num_applicants(3)
        
        # Course 2: no limit
        course2 = Course(
            "Programming Principles",
            "CS220",
            Major.CS,
            0,
            None,
            False,            
            semester,            
            3,
            False
        )
        course2.set_num_applicants(5)
        
        # Course 3: needs lottery - Major
        course3 = Course(
            "System Programming",
            "CS230",
            Major.CS,
            3,
            None,
            True,
            semester,            
            3,
            False
        )
        course3.set_num_applicants(5)
        
        # Course 4: needs lottery - Liberal Art
        course4 = Course(
            "Spanish Conversation",
            "HSS179",
            Major.HSS,
            3,
            None,
            True,
            semester,            
            3,            
            False
        )
        course4.set_num_applicants(5)        
        
        # Course 5: needs lottery - Other
        course5 = Course(
            "Basics of Artificial Intelligence<Physical AI>",
            "CoE202",
            Major.CoE,
            3,
            None,
            True,
            semester,            
            3,            
            False
        )
        course5.set_num_applicants(5)
        
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
                    None,
                    [course1, course2, course3, course4, course5],
                    [])
        student2 = Student("D", 
                    2020, 
                    Degree.BACHELOR, 
                    Major.CS,
                    None,
                    None,
                    [course2, course3, course4, course5],
                    [])
        students = [student1, copy.deepcopy(student1), copy.deepcopy(student1),\
                    student2, copy.deepcopy(student2)]

        # run the test
        prioritize_system = PrioritizeSystem(courses_dict)
        prioritized_students = prioritize_system.designate_priority(copy.deepcopy(students), (0.5, 0.4, 0.1))
        results = prioritize_system.register_students(copy.deepcopy(prioritized_students), (0.2, 0.2, 0.2))

        if PRINT_RESULT:
            pprint.pprint(students)
            print()
            pprint.pprint(prioritized_students)
            print()
            pprint.pprint(results)

        for course in [course1]:
            self.assertEqual(course.get_num_applicants(), 3)
        for course in [course2, course3, course4, course5]:
            self.assertEqual(course.get_num_applicants(), 5)

        applicants_dict = {course1.code:0, course2.code:0, course3.code:0, course4.code:0, course5.code:0}

        for student in results:
            for course in student.final_timetable:
                applicants_dict[course.code] += 1

        for course in [course2]: # no limit case
            self.assertEqual(applicants_dict[course.code], 5)
        for course in [course1, course3, course4, course5]:
            self.assertEqual(applicants_dict[course.code], 3)
    
if __name__ == "__main__":    
    unittest.main()