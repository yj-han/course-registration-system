from collections import defaultdict
from typing import Dict, List

from registration.course import Course
from registration.student import Degree, Student


def sum_of_credit(timetable: List[Course]) -> int:
    """Sum of credit of a timetable.

    Args:
        timetable (List[Course]): student's timetable.

    Returns:
        int: sum of credit
    """
    return sum(map(lambda x: x.credit, timetable))


def get_credit_distribution(bachelor_students: List[Student], max_credit: int=24) -> Dict[int, int]:
    """Get credit distribution of students' final timetables. (Only Bachelor)

    Args:
        students (List[Student]): List of students.
        max_credit (int): Maximum credit. Default is 24.

    Returns:
        Dict[int, int]: The credit distribution of students.
    """
    credit_distribution = defaultdict(int)
    assert all(student.degree == Degree.BACHELOR for student in bachelor_students)
            
    for student in bachelor_students:
        credits = sum_of_credit(student.final_timetable)
        if credits > max_credit:
            continue
        credit_distribution[credits] += 1

    return credit_distribution


