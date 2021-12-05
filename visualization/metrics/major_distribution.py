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
                MajorType.MAJOR: [0.4, 1, 1, ...],
                MajorType.DOUBLE_MAJOR: [0, 0.3, ...],
                MajorType.MINOR: [0.6, 0.4, ...],
                MajorType.ELSE: [0.1, 0.1, ...],
            },
        }
    """
    assert all(student.degree == Degree.BACHELOR for student in bachelor_students)
    major_distribution = {
        key: {
            MajorType.MAJOR: [],
            MajorType.DOUBLE_MAJOR: [],
            MajorType.MINOR: [],
            MajorType.ELSE: []
        } for key in major_filters
    }
    
    for student in bachelor_students:
        trial_credits = {
            key: 0 for key in major_filters
        }
        earned_credits = {
            key: 0 for key in major_filters
        }
        
        # Get courses that the student tried to register, but random
        for course in student.timetable:
            # If the course major is out of concern, skip it
            if not course.major in major_filters:
                continue
                        
            # If the course major does not need lottery, skip it
            if not course.is_lottery:
                continue
            
            # If the course is not major required nor major elective, skip it
            if not course.course_type == CourseType.MAJOR_REQUIRED and not course.course_type == CourseType.MAJOR_ELECTIVE:
                continue
            
            trial_credits[course.major] += course.credit
        
        for course in student.final_timetable:
            # If the course major is out of concern, skip it
            if not course.major in major_filters:
                continue
                        
            # If the course major does not need lottery, skip it
            if not course.is_lottery:
                continue
            
            # If the course is not major required nor major elective, skip it
            if not course.course_type == CourseType.MAJOR_REQUIRED and not course.course_type == CourseType.MAJOR_ELECTIVE:
                continue
            
            earned_credits[course.major] += course.credit
        

        for key in earned_credits.keys():            
            if trial_credits[key] == 0:
                continue
            
            student_major_type = MajorType.MAJOR
            if student.major == key:
                student_major_type = MajorType.MAJOR
            elif student.double_major == key:
                student_major_type = MajorType.DOUBLE_MAJOR
            elif student.minor == key:
                student_major_type = MajorType.MINOR
            else:
                student_major_type = MajorType.ELSE
                            
            major_distribution[key][student_major_type].append(earned_credits[key] / trial_credits[key])
            
    return major_distribution

