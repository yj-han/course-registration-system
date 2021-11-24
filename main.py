from registration.registration_system import *
from util.parse import parse_course_file, parse_student_file

if __name__ == "__main__":
    courses_dict = parse_course_file("2021 정규학기 과목별 추첨여부")
    students_dict = parse_student_file("2021 정규학기 수강신청 내역", courses_dict)
    
    students = list(students_dict.values())

    lottery_system = LotterySystem(courses_dict)
    students = lottery_system.register_students(students)

    # Change distributions to see various results
    major_priority_system = MajorPrioritySystem(courses_dict)
    students = major_priority_system.register_students(students, (0.3, 0.3, 0.1))

    # Change graduate standard and percentage to see various results
    grade_priority_system = GradePrioritySystem(courses_dict)
    students = grade_priority_system.register_students(students, 2018, 0.25)

    # Change distributions to see various results
    top3_priority_system = Top3PrioritySystem(courses_dict)
    students = top3_priority_system.designate_priority(students, (0.5, 0.4, 0.1))
    students = top3_priority_system.register_students(students, (0.2, 0.2, 0.2))