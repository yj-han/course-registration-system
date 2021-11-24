from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from registration.major import Major

class Semester(Enum):
    SPRING = "봄"
    FALL = "가을"

    
class Course:
    
    def __init__(self,
                 name: str, 
                 code: str,
                 major: Major,
                 capacity: int,
                 division: Optional[str],
                 is_lottery: bool,
                 semester: Semester = Semester.SPRING,
                 credit: int = 0,
                 applicants = [],    # Removed type annotation to avoid circular import between course.py and student.py
                 is_au: bool = False,
) -> None:
        """Initialization of Course. 
        Fields marked with * are not inserted at initialization.
        
        Args:
            name (str): name of course
            code (str): code of course
            major (Major): major of course
            capacity (int): capacity of course
            division (Optional[str]): division of course
            is_lottery (bool): is lottery of course
            semester (Semester, optional): semester of course. Defaults to SPRING.            
            *credit (int, optional): credit of course. Defaults to 0.
            *applicants (List[Student], optional): applicants of course. Defaults to [].
            *is_au (bool, optional): is_au of course. Defaults to False.
        """
        assert capacity >= 0 and len(applicants) >= 0
        
        self.name = name
        self.code = code    # Course code used here should be unique
        self.major = major
        self.capacity = capacity
        self.division = division
        self.is_lottery = is_lottery        
        self.semester = semester
        self.credit = credit
        self.applicants = applicants
        self.is_au = is_au

        self.num_applicants = len(applicants)

    def add_applicant(self, applicant) -> None:
        """Add applicant to course."""
        self.num_applicants += 1
        self.applicants.append(applicant)

    def __str__(self) -> str:
        return f"{self.name} \n\t code: {self.code} \n\t major: {self.major} \n\t capacity: {self.capacity} \n\t division: {self.division} \n\t is_lottery: {self.is_lottery} \n\t semester: {self.semester} \n\t credit: {self.credit} \n\t num_applicants: {self.num_applicants} \n\t is_au: {self.is_au}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Course):
            return False
        
        is_equal = self.code == other.code \
            and self.name == other.name \
            and self.major == other.major \
            and self.capacity == other.capacity \
            and self.division == other.division \
            and self.is_lottery == other.is_lottery \
            and self.semester == other.semester \
            and self.credit == other.credit \
            and self.num_applicants == other.num_applicants \
            and self.is_au == other.is_au
                
        return is_equal

    def __repr__(self):
        return str(self)
