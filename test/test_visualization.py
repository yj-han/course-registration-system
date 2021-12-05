import unittest

from registration.course import Course, CourseType, Semester
from registration.major import Major, MajorType
from registration.student import Student, Degree
from visualization.metrics.credit_distribution import get_credit_distribution, sum_of_credit
from visualization.metrics.grade_distribution import get_grade_distribution
from visualization.metrics.major_distribution import get_major_distribution

SEMESTER = Semester.FALL

class TestVisualization(unittest.TestCase):
    def test_sum_of_credit(self):
        timetable = [
            Course(
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
            ),
            Course(
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
            ),
            Course(
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
        ]
        
        self.assertEqual(sum_of_credit(timetable), 9)
    
    
    def test_get_credit_distribution(self):
        timetable = [
            Course(
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
            ),
            Course(
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
            ),
            Course(
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
        ]
        
        students = [
            Student("A",
                2020,
                Degree.BACHELOR,
                Major.CS,
                None,
                None,
                timetable,
                [timetable[0]]),
            Student("B",
                2018,
                Degree.BACHELOR,
                Major.BS,
                Major.EE,
                None,
                timetable,
                [timetable[0]]),
            Student("C",
                2021,
                Degree.BACHELOR,
                Major.PH,
                Major.NQE,
                None,
                timetable,
                timetable[:2]),
            Student("D",
                2016,
                Degree.BACHELOR,
                Major.CS,
                None,
                None,
                timetable,
                timetable[:2]),
            Student("E",
                2018,
                Degree.BACHELOR,
                Major.BS,
                Major.EE,
                None,
                timetable,
                timetable),
            Student("F",
                2017,
                Degree.BACHELOR,
                Major.PH,
                Major.NQE,
                None,
                timetable,
                timetable),
            Student("G",
                2021,
                Degree.BACHELOR,
                Major.PH,
                Major.NQE,
                None,
                timetable,
                timetable),
            Student("H",
                2019,
                Degree.BACHELOR,
                Major.PH,
                Major.NQE,
                None,
                timetable,
                []),
            Student("I",
                2020,
                Degree.BACHELOR,
                Major.PH,
                Major.NQE,
                None,
                timetable,
                []),
        ]
        
        credit_distribution = get_credit_distribution(students)
        self.assertEqual(credit_distribution, {0: 2, 3: 2, 6: 2, 9: 3})
        
    def test_get_grade_distribution(self):
        course_filters_dict = {
            "Logical Writing": lambda course: course.name == "논리적글쓰기",
            "AU": lambda course: course.is_au,
            "Basic Required": lambda course: course.course_type == CourseType.BASIC_REQUIRED,
            "All Lottery Courses": lambda course: course.is_lottery
        }

        timetable = [
            Course( # Logical Writing
                "논리적글쓰기",
                "HSS401",
                Major.HSS,
                3,
                None,
                False,
                SEMESTER,
                3,            
                False,
                CourseType.LIBERAL_ARTS_ELECTIVE
            ),
            Course( # AU & Lottery
                "코어운동",
                "HSS101",
                Major.HSS,
                1,
                None,
                True,
                SEMESTER,
                3,
                True,
                CourseType.LIBERAL_ARTS_ELECTIVE
            ),
            Course( # Basic Required
                "Intro to Chemistry",
                "CH101",
                Major.CH,
                0,
                None,
                False,
                SEMESTER,
                3,
                False,
                CourseType.BASIC_REQUIRED
            ),
            Course( # Lottery
                "Intro to Computer Science",
                "CS201",
                Major.HSS,
                3,
                None,
                True,
                SEMESTER,
                3,
                False,
                CourseType.LIBERAL_ARTS_REQUIRED
            ),
        ]
        
        students = [
            Student("A",
                2017,
                Degree.BACHELOR,
                Major.CS,
                None,
                None,
                timetable,
                timetable[:1]),
            Student("B",
                2018,
                Degree.BACHELOR,
                Major.BS,
                Major.EE,
                None,
                timetable,
                timetable[:2]),
            Student("C",
                2019,
                Degree.BACHELOR,
                Major.PH,
                Major.NQE,
                None,
                timetable,
                timetable[2:]),
            Student("D",
                2020,
                Degree.BACHELOR,
                Major.CS,
                None,
                None,
                timetable,
                timetable),
            Student("E",
                2021,
                Degree.BACHELOR,
                Major.BS,
                Major.EE,
                None,
                timetable,
                timetable)
        ]
    
        actual_grade_satisfaction_distribution = get_grade_distribution(students, course_filters_dict)
        expected_grade_satisfaction_distribution = {
            "Logical Writing": {
                "Above Threshold": 2,
                "Below Threshold": 2,
            },
            "AU": {
                "Above Threshold": 1,
                "Below Threshold": 2,
            },
            "Basic Required": {
                "Above Threshold": 0,
                "Below Threshold": 3,
            },
            "All Lottery Courses": {
                "Above Threshold": 1,
                "Below Threshold": 5,
            },
        }

        self.assertEqual(expected_grade_satisfaction_distribution, actual_grade_satisfaction_distribution)
        
    def test_get_major_distribution(self):
        timetable = [
            Course( # CS
                "Computer Systems",
                "CS101",
                Major.CS,
                1,
                None,
                True,
                SEMESTER,
                3,
                True,
                CourseType.MAJOR_ELECTIVE
            ),
            Course( # EE
                "Intro to Circuit Theory",
                "EE201",
                Major.EE,
                0,
                None,
                False,
                SEMESTER,
                3,
                False,
                CourseType.MAJOR_REQUIRED
            ),
            Course( # Lottery
                "Intro to Computer Science",
                "CS101",
                Major.CS,
                3,
                None,
                True,
                SEMESTER,
                3,
                False,
                CourseType.BASIC_REQUIRED
            ),
        ]
        
        students = [
            Student("A",
                2017,
                Degree.BACHELOR,
                Major.CS,
                None,
                None,
                timetable,
                timetable[:1]),
            Student("B",
                2018,
                Degree.BACHELOR,
                Major.BS,
                Major.EE,
                None,
                timetable,
                timetable),
            Student("C",
                2019,
                Degree.BACHELOR,
                Major.EE,
                Major.NQE,
                None,
                timetable,
                timetable[2:]),
            Student("D",
                2020,
                Degree.BACHELOR,
                Major.CS,
                None,
                None,
                timetable,
                timetable),
            Student("E",
                2021,
                Degree.BACHELOR,
                Major.BS,
                None,
                Major.EE,
                timetable,
                timetable)
        ]
        
        actual_major_distribution = get_major_distribution(students)
        expected_major_distribution = {
            Major.CS: {
                "Computer Systems": {
                    MajorType.MAJOR: 2,
                    MajorType.MINOR: 0,
                    MajorType.DOUBLE_MAJOR: 0,
                    MajorType.ELSE: 2,
                },
            },
            Major.EE: {}
        }

        self.assertEqual(expected_major_distribution, actual_major_distribution)
    
if __name__ == "__main__":
    unittest.main()