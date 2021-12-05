from typing import Dict, List

from registration.registration_system.system_type import SystemType
from registration.student import Degree, Student
from registration.major import MajorType
from registration.course import CourseType


def get_reactiveness_distribution(bachelor_students: List[Student]) -> list:
    """Get the distribution of each student's top 3 success rate.

    Args:
        bachelor_students (List[Student]): bachelor students
        major_filters (list, optional): Selected majors. Defaults to [Major.CS].

    Returns:
        list: satisfaction distribution
    """
    assert all(student.degree == Degree.BACHELOR for student in bachelor_students)
    
    top3_distribution = []
    for student in bachelor_students:
        top3_courses = student.timetable[:3]
        
        earned_coures = 0
        for course in student.final_timetable:
            if course not in top3_courses:
                continue
            
            earned_coures += 1
        
        top3_distribution.append(earned_coures)
        
    return top3_distribution
