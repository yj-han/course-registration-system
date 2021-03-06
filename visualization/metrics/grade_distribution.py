from collections import defaultdict
from typing import Dict, List

from registration.student import Degree, Student

course_filters_dict = {
    # "Logical Writing": lambda course: course.name == "논리적글쓰기",
    # "AU": lambda course: course.is_au,
    # "Basic Required": lambda course: course.course_type == CourseType.BASIC_REQUIRED,
    "All Lottery Courses": lambda course: course.is_lottery
}

def get_grade_distribution(bachelor_students: List[Student], 
                           course_filters_dict: Dict[str, callable],
                           threshold=2021) -> Dict[str, Dict[str, int]]:
    """Get grade satisfaction distribution for course restraints.

    Args:
        bachelor_students (List[Student]): [description]
        course_filters_dict (Dict[str, function]): [description]
        threshold (int, optional): [description]. Defaults to 2022.

    Returns:
        Dict[str, Dict[int, int]]: grade satisfaction distribution
        ex)
        dict = {
            "label": {
                "Above threshold": [13, 2, 6, ...],
                "Below threshold": [1, 3, 10, ...]
            },
            ...            
        }
    """
    assert all(student.degree == Degree.BACHELOR for student in bachelor_students)
    
    grade_satisfaction_distribution = dict()
    for key in course_filters_dict.keys():
        grade_satisfaction_distribution[key] = defaultdict(list)
    
    for student in bachelor_students:
        age = threshold - student.year + 1
        grade = "Below Threshold" if age < 4 else "Above Threshold"
        
        earned_credits = 0
        for course in student.final_timetable:
            if not course.is_lottery:
                continue
            
            for label, restraint_function in course_filters_dict.items():
                if restraint_function(course):
                    earned_credits += course.credit
                                    
        grade_satisfaction_distribution[label][grade].append(earned_credits)
               
    return grade_satisfaction_distribution
