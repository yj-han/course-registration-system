import copy
from registration.course import Semester
from registration.registration_system import top3_based_1_system
from registration.registration_system.lottery_system import LotterySystem
from registration.registration_system.major_priority_system import MajorPrioritySystem
from registration.registration_system.grade_priority_system import GradePrioritySystem
from registration.registration_system.top3_priority_system import Top3PrioritySystem
from registration.registration_system.top3_based_1_system import Top3Based1System
from util.parse import parse_course_file, parse_student_file

if __name__ == "__main__":
    courses_dict = parse_course_file("2021 정규학기 과목별 추첨여부.xlsx", "2021 봄학기 과목.xls", Semester.SPRING)
    students_dict = parse_student_file("2021 정규학기 수강신청 내역.xlsx", courses_dict, Semester.SPRING)
    
    students = list(students_dict.values())

    lottery_system = LotterySystem(copy.deepcopy(courses_dict))
    result_students = lottery_system.register_students(copy.deepcopy(students))
    
    print(result_students[:5])
    
    # Change distributions to see various results
    major_priority_system = MajorPrioritySystem(copy.deepcopy(courses_dict))
    result_students = major_priority_system.register_students(copy.deepcopy(students), (0.3, 0.3, 0.1))

    print(result_students[:5])    

    # Change graduate standard and probability to see various results
    grade_priority_system = GradePrioritySystem(copy.deepcopy(courses_dict))
    result_students = grade_priority_system.register_students(copy.deepcopy(students), 2018, 0.25)
    
    print(result_students[:5])

    # Change distributions to see various results
    top3_priority_system = Top3PrioritySystem(copy.deepcopy(courses_dict))
    prioritized_students = top3_priority_system.designate_priority(copy.deepcopy(students), (0.5, 0.4, 0.1))
    result_students = top3_priority_system.register_students(prioritized_students, (0.2, 0.2, 0.2))

    print(result_students[:5])

    # Change distributions to see various results
    top3_based_1_system = Top3Based1System(copy.deepcopy(courses_dict))
    prioritized_students = top3_based_1_system.designate_priority(copy.deepcopy(students), (0.5, 0.4, 0.1))
    result_students = top3_based_1_system.register_students(prioritized_students, (0.2, 0.2, 0.2), 0.3, 0.3, 2018)

    print(result_students[:5])