from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from registration.major import Major

class Semester(str, Enum):
    SPRING = "봄"
    FALL = "가을"
    

class CourseType(str, Enum):
    MAJOR_REQUIRED = "전공필수"
    MAJOR_ELECTIVE = "전공선택"
    BASIC_REQUIRED = "기초필수"
    BASIC_ELECTIVE = "기초선택"    
    LIBERAL_ARTS_REQUIRED = "교양필수"
    LIBERAL_ARTS_ELECTIVE = "교양선택" # 원래 인문사회선택
    COMMON_REQUIRED = "공통필수"
    RESEARCH = "연구"
    SEMINAR = "세미나"
    UNRESTRICTED_ELECTIVE = "자유선택"
    ELSE = "기타"


    @classmethod
    def value_of(cls, value):
        search_value = ""
        
        if "필수" in value:
            search_value = "필수"
        if "선택" in value:
            search_value = "선택"            
            
        if "전공" in value:
            search_value = "전공" + search_value
        if "인문사회" in value or "교양" in value:
            search_value = "교양" + search_value
        if "자유" in value:
            search_value = "자유" + search_value   
        if "기초" in value:
            search_value = "기초" + search_value
        if "공통" in value:
            search_value = "공통" + search_value
        
        if "연구" in value:
            search_value = "연구"
        if "세미나" in value:
            search_value = "세미나"
            
        for enum in cls.__members__.values():
            if search_value == enum.value:
                return enum
        else:
            return cls.ELSE
    
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
                 is_au: bool = False,
                 course_type: CourseType = CourseType.ELSE,                 
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
            *is_au (bool, optional): is_au of course. Defaults to False.
            *course_type (CourseType, optional): course_type of course. Defaults to ELSE.
        """
        assert capacity >= 0
        
        self.name = name
        self.code = code    # Course code used here should be unique
        self.major = major
        self.capacity = capacity
        self.division = division
        self.is_lottery = is_lottery        
        self.semester = semester
        self.credit = credit
        self.is_au = is_au
        self.course_type = course_type        
        self.__num_applicants = 0

    def add_num_applicants(self) -> None:
        self.__num_applicants += 1
        
    def get_num_applicants(self) -> int:
        return self.__num_applicants

    def set_num_applicants(self, num_applicants: int) -> None:
        self.__num_applicants = num_applicants

    def __str__(self) -> str:
        return f"{self.name} \n\t code: {self.code} \n\t major: {self.major} \n\t capacity: {self.capacity} \n\t division: {self.division} \n\t is_lottery: {self.is_lottery} \n\t semester: {self.semester} \n\t credit: {self.credit} \n\t num_applicants: {self.get_num_applicants()} \n\t is_au: {self.is_au} \n\t course_type: {self.course_type}"
    
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
            and self.is_au == other.is_au \
            and self.course_type == other.course_type \
                                
        return is_equal

    def __repr__(self):
        return str(self)
