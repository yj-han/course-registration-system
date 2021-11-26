import copy
from registration.course import Semester
from registration.registration_system import *
from util.parse import parse_course_file, parse_student_file, generate_course_type_enum
from visualization.evaluation import evaluation

import pickle

if __name__ == "__main__":
    # courses_dict = parse_course_file("2021 정규학기 과목별 추첨여부.xlsx", "2021 봄학기 과목.xls", Semester.SPRING)
    # students_dict = parse_student_file("2021 정규학기 수강신청 내역.xlsx", courses_dict, Semester.SPRING)
    
    # students = list(students_dict.values())

    # results = {}
    # lottery_system = LotterySystem(copy.deepcopy(courses_dict))
    # result_students = lottery_system.register_students(copy.deepcopy(students))
    # results['lottery'] = result_students

    # # Change distributions to see various results
    # major_priority_system = MajorPrioritySystem(copy.deepcopy(courses_dict))
    # result_students = major_priority_system.register_students(copy.deepcopy(students), (0.3, 0.3, 0.1))
    # results['major priority'] = result_students

    # # Change graduate standard and percentage to see various results
    # grade_priority_system = GradePrioritySystem(copy.deepcopy(courses_dict))
    # result_students = grade_priority_system.register_students(copy.deepcopy(students), 2018, 0.25)
    # results['grade priority'] = result_students

    # # Change distributions to see various results
    # top3_priority_system = Top3PrioritySystem(copy.deepcopy(courses_dict))
    # prioritized_students = top3_priority_system.designate_priority(copy.deepcopy(students), (0.5, 0.4, 0.1))
    # result_students = top3_priority_system.register_students(prioritized_students, (0.2, 0.2, 0.2))
    # results['top3 priority'] = result_students

    # with open('results.pickle', 'wb') as f:
    #     pickle.dump(results, f)
    
    with open('results.pickle', 'rb') as f:
        results = pickle.load(f)

    evaluation(results)
