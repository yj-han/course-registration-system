import unittest

from registration.course import Course, Semester
from registration.major import Major
from registration.student import Degree, Student
from util.parse import parse_course_file, parse_student_file


class TestParse(unittest.TestCase):
    def test_parse_course_file(self):
        semester = Semester.FALL

        expected_course1 = Course(
            "URP(학부생연구참여)(B)",
            "URP490AA",
            Major.URP,
            1,
            "AA",
            False,
            semester,
            3,
            False
        )  
        expected_course2 = Course(
            "Intermediate English Reading & Writing",
            "HSS011B",
            Major.HSS,
            20,
            "B",
            False,
            semester,
            2,
            False
        )
        expected_course3 = Course(
            "체력육성",
            "HSS051C",
            Major.HSS,
            30,
            "C",
            True,
            semester,
            0,
            True,
        )
        expected_course4 = Course(
            "역사학 특강<고고학 발굴과 분석의 이해>",
            "HSS304A",
            Major.HSS,
            30,
            "A",            
            True,
            semester,
            3,
            False
        )

        courses_dict = parse_course_file("2021 정규학기 과목별 추첨여부.xlsx", "2021 가을학기 과목.xls", Semester.FALL)
        
        self.assertEqual(courses_dict[expected_course1.code], expected_course1)
        self.assertEqual(courses_dict[expected_course2.code], expected_course2)
        self.assertEqual(courses_dict[expected_course3.code], expected_course3)
        self.assertEqual(courses_dict[expected_course4.code], expected_course4)       

    def test_parse_student_file(self):
        # row 2 in the excel file
        expected_student1 = Student(
            "2017350fc2ea55f4e71ed7891323d17f74af",
            2017,
            Degree.BACHELOR,
            Major.CBE,
            None,
            Major.MS,
        )
        registered_course_code1 = "CBE496"
        
        # row 120 in the excel file
        expected_student2 = Student(
            "20211f7159f967f1610e1c4acc319ea2ee29",
            2021,
            Degree.BACHELOR,
            Major.FRESH,
            None,
            None,
        )
        registered_course_code2 = "HSS09110" # class 10

        # row 342 in the excel file
        expected_student3 = Student(
            "2020111c25224ee0333170668ffd8ef2d755",
            2020,
            Degree.BACHELOR,
            Major.EE,
            None,
            None,
        )
        registered_course_code3 = "EE210A"
        
        # row 19688 in the excel file
        expected_student4 = Student(
            "2021b526709b2f64d3ce5a9266876990a22f",
            2021,
            Degree.DOCTOR,
            Major.CS,
            None,
            None,
        )
        registered_course_code4 = "MSB441"
        
        courses_dict = parse_course_file("2021 정규학기 과목별 추첨여부.xlsx", "2021 가을학기 과목.xls", Semester.FALL)
        students_dict = parse_student_file("2021 정규학기 수강신청 내역.xlsx", courses_dict, Semester.FALL)

        self.assertEqual(students_dict[expected_student1.id], expected_student1)
        self.assertEqual(students_dict[expected_student2.id], expected_student2)
        self.assertEqual(students_dict[expected_student3.id], expected_student3)
        self.assertEqual(students_dict[expected_student4.id], expected_student4)
        
if __name__ == "__main__":
    unittest.main()