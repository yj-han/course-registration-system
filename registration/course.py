from typing import Optional

from registration.major import Major

class Course:
    
    def __init__(self, 
                 name: str, 
                 code: str,
                 major: Major,
                 credit: int,
                 capacity: int,
                 division: Optional[str],
                 num_applicants: int, 
                 is_lottery: bool, 
                 is_au: bool) -> None:
        """Initialization of Course

        Args:
            name (str): name of the course
            code (str): code of the course
            major (Major): major of the course
            credit (int): credit of the course
            capacity (int): capacity of the course
            division (Optional[str]): division of the course
            num_applicants (int): number of applicants of the course
            is_lottery (bool): whether the course is lottery
            is_au (bool): whether the course is AU
        """

        assert capacity >= 0 and num_applicants >= 0
        
        self.name = name
        self.code = code
        self.credit = credit
        self.major = major
        self.capacity = capacity
        self.division = division
        self.num_applicants = num_applicants
        self.is_lottery = is_lottery
        self.is_au = is_au

    def __str__(self) -> str:
        return f"code: {self.code}, capacity: {self.capacity}, num_applicants: {self.num_applicants}, is_lottery: {self.is_lottery}"

    def __repr__(self):
        return str(self)