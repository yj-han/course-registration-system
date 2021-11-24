import unittest

from registration.course import Course
from registration.major import Major
from registration.registration_system import LotterySystem
from registration.registration_system import GradePrioritySystem
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
            0,
            False,
            False
        )
        # Course 2: needs lottery        
        course2 = Course(
            "Intro to Biology",
            "BS101",
            Major.BS,
            3,
            1,
            None,
            0,
            True,
            False
        )
        # Course 3: no limit
        course3 = Course(
            "Intro to Chemistry",
            "CH101",
            Major.CS,
            3,
            0,
            None,
            0,
            False,
            False
        )
        courses_dict = {
            course1.code: course1,
            course2.code: course2, 
            course3.code: course3
        }
        
        student1 = Student("A", 
                    2020, 
                    Degree.BACHELOR, 
                    Major.CS,
                    None, 
                    [course2, course1, course3],
                    [])
        student2 = Student("B", 
                    2018, 
                    Degree.DOCTOR, 
                    Major.BS,
                    Major.EE, 
                    [course3, course1, course2],
                    [])
        student3 = Student("C", 
                    2021, 
                    Degree.MASTER, 
                    Major.PH,
                    Major.NQE, 
                    [course1, course2, course3],
                    [])
        students = [student1, student2, student3]

        # run the test
        lottery_system = LotterySystem(courses_dict)
        results = lottery_system.register_students(students)
                    
        for course in courses_dict.values():
            self.assertEqual(course.num_applicants, 3)

        sorted_results = sorted(results, key=lambda x: len(x.final_timetable))
        # only one student should be assigned to course 2
        lucky_student = sorted_results[2]
        self.assertIn(course2, lucky_student.final_timetable)
        
        # other students should be assigned to course 1 and course 3
        self.assertEqual(sorted_results[0].final_timetable, [course1, course3])
        self.assertEqual(sorted_results[1].final_timetable, [course1, course3])       

    def test_grade_priority_system(self):
        # Course 1: does not need lottery
        course1 = Course(
            "Intro to Computer Science",
            "CS101",
            Major.CS,
            3,
            9,
            None,
            0,
            False,
            False
        )
        # Course 2: needs lottery
        course2 = Course(
            "Intro to Biology",
            "BS101",
            Major.BS,
            3,
            4,
            None,
            0,
            True,
            False
        )
        # Course 3: no limit
        course3 = Course(
            "Intro to Chemistry",
            "CH101",
            Major.CS,
            3,
            0,
            None,
            0,
            False,
            False
        )
        courses_dict = {
            course1.code: course1,
            course2.code: course2,
            course3.code: course3
        }

        student1 = Student("A",
                           2020,
                           Degree.BACHELOR,
                           Major.CS,
                           None,
                           [course2, course1, course3],
                           [])
        student2 = Student("B",
                           2018,
                           Degree.DOCTOR,
                           Major.BS,
                           Major.EE,
                           [course3, course1, course2],
                           [])
        student3 = Student("C",
                           2021,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           [course1, course2, course3],
                           [])
        student4 = Student("D",
                           2016,
                           Degree.BACHELOR,
                           Major.CS,
                           None,
                           [course2, course1, course3],
                           [])
        student5 = Student("E",
                           2018,
                           Degree.DOCTOR,
                           Major.BS,
                           Major.EE,
                           [course3, course1, course2],
                           [])
        student6 = Student("F",
                           2017,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           [course1, course2, course3],
                           [])
        student7 = Student("G",
                           2021,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           [course1, course2, course3],
                           [])
        student8 = Student("H",
                           2019,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           [course1, course2, course3],
                           [])
        student9 = Student("I",
                           2020,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           [course1, course2, course3],
                           [])
        students = [student1, student2, student3, student4, student5, student6, student7, student8, student9]

        # run the test
        grade_priority_system = GradePrioritySystem(courses_dict)
        graduate_standard = 2018
        priority_percentage = 25
        results = grade_priority_system.register_students(students, graduate_standard, priority_percentage)

        lucky_students = []
        for student in results:
            self.assertIn(course1, student.final_timetable)
            self.assertIn(course3, student.final_timetable)
            if course2 in student.final_timetable:
                lucky_students.append(student)
        self.assertEqual(len(lucky_students), course2.capacity)

        priority_count = 0
        for lucky in lucky_students:
            if lucky.year <= graduate_standard:
                priority_count += 1
        self.assertGreaterEqual(priority_count, int(course2.capacity * priority_percentage / 100))
if __name__ == "__main__":
    unittest.main()