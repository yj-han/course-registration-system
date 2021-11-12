class Course:
    
    def __init__(self, 
                 name: str, 
                 code: str, 
                 credit: int,
                 capacity: int, 
                 num_applicants: int, 
                 is_lottery: bool, 
                 is_mandatory: bool,
                 is_au: bool) -> None:
        """Initialization

        Args:
            name (str): [description]
            code (str): [description]
            credit (int): [description]
            capacity (int): [description]
            num_applicants (int): [description]
            is_lottery (bool): [description]
            is_mandatory (bool): [description]
            is_au (bool): [description]
        """

        assert capacity >= 0 and num_applicants >= 0
        
        self.name = name;
        self.code = code;
        # TODO: 요청하지는 않았으나 중요하지는 않음.. 넣을지 말지 정하면 좋을듯
        self.credit = credit;
        self.capacity = capacity;
        self.num_applicants = num_applicants;
        self.is_lottery = is_lottery;
        # TODO: 전필인지 아닌지 요청하는 거 까먹음...! 요청드리기 죄송하면 직접 발품팔아도 괜찮음...
        self.is_mandatory = is_mandatory;
        self.is_au = is_au;

