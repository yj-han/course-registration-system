import unittest
import copy

from registration.course import Course, CourseType, Semester
from registration.major import Major
from registration.registration_system.lottery_system import LotterySystem
from registration.registration_system.grade_priority_system import GradePrioritySystem
from registration.registration_system.top3_priority_system import Top3PrioritySystem
from registration.student import Degree, Student

SEMESTER = Semester.FALL
class TestRegistrationSystem(unittest.TestCase):
    def test_lottery_system(self):
        # Course 1: does not need lottery
        course1 = Course(
            "Intro to Computer Science",
            "CS101",
            Major.CS,
            3,
            None,
            False,
            SEMESTER,
            3,            
            False,
            CourseType.MAJOR_REQUIRED
        )
        # Course 2: needs lottery        
        course2 = Course(
            "Intro to Biology",
            "BS101",
            Major.BS,
            1,
            None,
            True,
            SEMESTER,
            3,
            False,
            CourseType.MAJOR_REQUIRED
        )
        # Course 3: no limit
        course3 = Course(
            "Intro to Chemistry",
            "CH101",
            Major.CS,
            0,
            None,
            False,
            SEMESTER,
            3,
            False,
            CourseType.MAJOR_REQUIRED
        )
        
        course1.set_num_applicants(3)
        course2.set_num_applicants(3)
        course3.set_num_applicants(3)
        
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
                    None, 
                    [course2, course1, course3],
                    [])
        student2 = Student("B", 
                    2018, 
                    Degree.DOCTOR, 
                    Major.BS,
                    Major.EE, 
                    None,
                    [course3, course1, course2],
                    [])
        student3 = Student("C", 
                    2021, 
                    Degree.MASTER,
                    Major.PH,
                    Major.NQE, 
                    None, 
                    [course1, course2, course3],
                    [])
        students = [student1, student2, student3]

        # run the test
        lottery_system = LotterySystem(courses_dict)
        results = lottery_system.register_students(students)
        
        for course in courses_dict.values():
            self.assertEqual(course.get_num_applicants(), 3)

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
            None,
            False,
            SEMESTER,
            3,            
            False,
            CourseType.MAJOR_REQUIRED,
        )
        # Course 2: needs lottery        
        course2 = Course(
            "Intro to Biology",
            "BS101",         
            Major.BS,
            1,
            None,
            True,
            SEMESTER,
            3,
            False,
            CourseType.MAJOR_REQUIRED,   
        )
        # Course 3: no limit
        course3 = Course(
            "Intro to Chemistry",
            "CH101",
            Major.CS,
            0,
            None,
            False,
            SEMESTER,
            3,
            False,
            CourseType.MAJOR_REQUIRED
        )
        
        course1.set_num_applicants(9)
        course2.set_num_applicants(9)
        course3.set_num_applicants(9)
        
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
                           None,
                           [course2, course1, course3],
                           [])
        student2 = Student("B",
                           2018,
                           Degree.DOCTOR,
                           Major.BS,
                           Major.EE,
                           None,
                           [course3, course1, course2],
                           [])
        student3 = Student("C",
                           2021,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           None,
                           [course1, course2, course3],
                           [])
        student4 = Student("D",
                           2016,
                           Degree.BACHELOR,
                           Major.CS,
                           None,
                           None,
                           [course2, course1, course3],
                           [])
        student5 = Student("E",
                           2018,
                           Degree.DOCTOR,
                           Major.BS,
                           Major.EE,
                           None,
                           [course3, course1, course2],
                           [])
        student6 = Student("F",
                           2017,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           None,
                           [course1, course2, course3],
                           [])
        student7 = Student("G",
                           2021,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           None,
                           [course1, course2, course3],
                           [])
        student8 = Student("H",
                           2019,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           None,
                           [course1, course2, course3],
                           [])
        student9 = Student("I",
                           2020,
                           Degree.MASTER,
                           Major.PH,
                           Major.NQE,
                           None,
                           [course1, course2, course3],
                           [])
        students = [student1, student2, student3, student4, student5, student6, student7, student8, student9]

        # run the test
        grade_priority_system = GradePrioritySystem(courses_dict)
        graduate_standard = 2018
        priority_percentage = 0.25
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

    def test_top3_priority_system(self):
        # Course 1: does not need lottery
        course1 = Course(
            "Intro to Computer Science",
            "CS101",
            Major.CS,
            3,
            None,
            False,
            SEMESTER,
            3,            
            False,
            CourseType.MAJOR_REQUIRED
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
            SEMESTER,            
            3,            
            False,
            CourseType.MAJOR_ELECTIVE
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
            SEMESTER,            
            3,
            False,
            CourseType.MAJOR_ELECTIVE
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
            SEMESTER,
            3,            
            False,
            CourseType.LIBERAL_ARTS_ELECTIVE            
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
            SEMESTER,
            3,
            False,
            CourseType.BASIC_ELECTIVE            
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
        prioritize_system = Top3PrioritySystem(courses_dict)
        prioritized_students = prioritize_system.designate_priority(students, (0.5, 0.4, 0.1))
        results = prioritize_system.register_students(prioritized_students, (0.2, 0.2, 0.2))
                    
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