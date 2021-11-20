from registration.registration_system import LotterySystem
from util.parse import parse_course_file, parse_student_file

if __name__ == "__main__":
    courses_dict = parse_course_file("2021 정규학기 과목별 추첨여부")
    students_dict = parse_student_file("2021 정규학기 수강신청 내역", courses_dict)
    
    students = list(students_dict.values())

    lottery_system = LotterySystem(courses_dict)
    students = lottery_system.register_students(students)
