from typing import Optional


class Course:
    
    def __init__(self, 
                 name: str, 
                 code: str,
                 credit: int,
                 capacity: int,
                 division: Optional[str],
                 num_applicants: int, 
                 is_lottery: bool, 
                 is_au: bool) -> None:
        """Initialization of Course

        Args:
            name (str): [description]
            code (str): [description]
            credit (int): [description]
            capacity (int): [description]
            division (Optional[str]): [description]            
            num_applicants (int): [description]
            is_lottery (bool): [description]
            is_mandatory (bool): [description]
            is_au (bool): [description]
        """

        assert capacity >= 0 and num_applicants >= 0
        
        self.name = name;
        self.code = code;
        self.credit = credit;
        self.capacity = capacity;
        self.division = division;
        self.num_applicants = num_applicants;
        self.is_lottery = is_lottery;
        self.is_au = is_au;
