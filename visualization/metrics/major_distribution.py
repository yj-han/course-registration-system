from collections import defaultdict
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from registration.student import Degree, Student
from registration.major import Major, MajorType
from registration.course import CourseType


def get_major_distribution(bachelor_students: List[Student], 
                           major_filters=[Major.CS, Major.EE]) -> Dict[Major, Dict[str, Dict[MajorType, int]]]:
    """Get the distribution of each major.

    Args:
        bachelor_students (List[Student]): bachelor students
        major_filters (list, optional): Selected majors. Defaults to [Major.CS, Major.EE].

    Returns:
        Dict[str, Dict[str, int]]: major satisfaction distribution
        ex)
        dict = {
            Major.CS: {
                "Introduction to Computer Science": {
                    MajorType.MAJOR: 13,
                    MajorType.DOUBLE_MAJOR: 7,
                    MajorType.MINOR: 6,
                    MajorType.ELSE: 10                      
                },
                "Computer Systems": {
                    MajorType.MAJOR: 13,
                    MajorType.DOUBLE_MAJOR: 7,
                    MajorType.MINOR: 6,
                    MajorType.ELSE: 10                      
                },
                ...
            },
            ...
        }
    """
    assert all(student.degree == Degree.BACHELOR for student in bachelor_students)
    major_distribution = {key: defaultdict(dict) for key in major_filters}
    
    for student in bachelor_students:
        for course in student.final_timetable:
            course_major = course.major
            
            # If the course major is out of concern, skip it
            if not course_major in major_filters:
                continue
                        
            # If the course major does not need lottery, skip it
            if not course.is_lottery:
                continue
            
            # If the course is not major required nor major elective, skip it
            if not course.course_type == CourseType.MAJOR_REQUIRED and not course.course_type == CourseType.MAJOR_ELECTIVE:
                continue
            
            if course.name not in major_distribution[course_major].keys():
                major_distribution[course_major][course.name] = {
                    MajorType.MAJOR: 0,
                    MajorType.DOUBLE_MAJOR: 0,
                    MajorType.MINOR: 0,
                    MajorType.ELSE: 0
                }
            
            if student.major == course_major:
                major_distribution[course_major][course.name][MajorType.MAJOR] += 1
            elif student.double_major == course_major:
                major_distribution[course_major][course.name][MajorType.DOUBLE_MAJOR] += 1
            elif student.minor == course_major:
                major_distribution[course_major][course.name][MajorType.MINOR] += 1
            else:
                major_distribution[course_major][course.name][MajorType.ELSE] += 1

    return major_distribution

