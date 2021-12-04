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
                 double_major: Optional[Major] = None,
                 minor: Optional[Major] = None, 
                 timetable: List[Course] = [],
                 final_timetable: List[Course] = []) -> None:
        """Initialization of Student

        Args:
            id (str): unique token
            year (int): year of entrance
            degree (Degree): level of degree
            major (Major): major of student
            double_major (Optional[Major]): double_major if exists else None            
            minor (Optional[Major]): minor if exists else None
            timetable (List[Course]): a list of courses registered
            final_timetable (List[Course]): a list of courses finally set
        """
        self.id = id
        self.year = year
        self.degree = degree
        self.major = major
        self.double_major = double_major
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
        return f"\n{self.id} \n\t year: {self.year} \n\t degree: {self.degree} \n\t major: {self.major} \n\t length of timetable: {len(self.timetable)} \n\t length of final timetable: {len(self.final_timetable)}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return False
        
        is_equal = self.id == other.id \
            and self.year == other.year \
            and self.degree == other.degree \
            and self.major == other.major \
            and self.double_major == other.double_major \
            and self.minor == other.minor
        
        return is_equal
    
    def __repr__(self):
        return str(self)