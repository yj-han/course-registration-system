import unittest

from registration.course import Course, Semester
from registration.major import Major
from util.parse import parse_course_file


class TestParse(unittest.TestCase):
    def test_parse_course_file(self):
        semester = Semester.FALL

        # course1_index = 0
        expected_course1 = Course(
            "URP(학부생연구참여)(B)",
            "URP490AA",
            Major.URP,
            1,
            "AA",
            False,
            semester,
            3,
            0,
            False
        )  
        # course2_index = 60
        expected_course2 = Course(
            "Intermediate English Reading & Writing",
            "HSS011B",
            Major.HSS,
            20,
            "B",
            False,
            semester,
            2,
            0,
            False
        )
        # course3_index = 100
        expected_course3 = Course(
            "체력육성",
            "HSS051C",
            Major.HSS,
            30,
            "C",
            True,
            semester,
            0,
            0,
            True,
        )
        # course4_index = 240
        expected_course4 = Course(
            "역사학 특강<고고학 발굴과 분석의 이해>",
            "HSS304A",
            Major.HSS,
            30,
            "A",            
            True,
            semester,
            3,
            0,
            False
        )

        expected_courses_dict = {
            expected_course1.code: expected_course1, 
            expected_course2.code: expected_course2, 
            expected_course3.code: expected_course3,
            expected_course4.code: expected_course4
        }
        
        courses_dict = parse_course_file("2021 정규학기 과목별 추첨여부.xlsx", "2021 가을학기 과목.xls", Semester.FALL)
        
        self.assertEqual(expected_courses_dict[expected_course1.code], courses_dict[expected_course1.code])
        self.assertEqual(expected_courses_dict[expected_course2.code], courses_dict[expected_course2.code])
        self.assertEqual(expected_courses_dict[expected_course3.code], courses_dict[expected_course3.code])
        self.assertEqual(expected_courses_dict[expected_course4.code], courses_dict[expected_course4.code])        

    def test_parse_student_file(self):
        pass
    
if __name__ == "__main__":
    unittest.main()