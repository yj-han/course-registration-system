from enum import Enum, unique
from typing import List, Optional

from registration.course import Course
from registration.major import Major


@unique
class Degree(str, Enum):
    BACHELOR = "학사과정"
    MASTER = "석사과정"
    DOCTOR = "박사과정"
    ELSE = "기타"
    
    @classmethod
    def value_of(cls, value):
        if "학사" in value:
            return cls.BACHELOR
        elif "석사" in value:
            return cls.MASTER
        elif "박사" in value:
            return cls.DOCTOR
        else:
            return cls.ELSE
        
        
class Student:
    
    def __init__(self, 
                 id: str,
                 year: int,
                 degree: Degree,
                 major: Major, 
                 minor: Optional[Major] = None, 
                 timetable: List[Course] = [], 
                 final_timetable: List[Course] = []) -> None:
        """Initialization of Student

        Args:
            id (str): unique token
            year (int): year of entrance
            degree (Degree): level of degree
            major (Major): major of student
            minor (Optional[Major]): minor if exists else None
            timetable (List[Course]): a list of courses registered
            final_timetable (List[Course]): a list of courses finally set
        """
        self.id = id
        self.year = year
        self.degree = degree
        self.major = major
        self.minor = minor
        self.timetable = timetable
        self.final_timetable = final_timetable

    def add_to_timetable(self, course: Course) -> None:
        """Add course to final timetable

        Args:
            course (Course): course to add
        """
        self.timetable.append(course)    

    def add_to_final_timetable(self, course: Course) -> None:
        """Add course to final timetable

        Args:
            course (Course): course to add
        """
        self.final_timetable.append(course)
    
    def __str__(self) -> str:
        return f"""id: {self.id}, year: {self.year}, degree: {self.degree}, 
            major: {self.major}, # timetable: {len(self.timetable)},  # final timetable: {len(self.final_timetable)}"""
        