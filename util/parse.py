import sys
from typing import List
import pandas as pd
from pathlib import Path

# TODO: registration 같은 내 폴더를 쉽게 import하는 법을 모르겠어용,,, help
# root_path = Path("./registration/").resolve()
# print(root_path)
# if root_path not in sys.path:
#     sys.path.append(root_path)
    
from registration.student import Student
from registration.course import Course

DATA_PATH = "./data/"
EXCEL_EXT = ".xlsx"


def parse_student_file(filename: str) -> List[Student]:
    """Parse a student data file with `filename`

    Args:
        filename (str): the name of the file

    Returns:
        List[Student]: a list of `Student` objects
    """
    filename = filename if EXCEL_EXT in filename else filename + EXCEL_EXT
    data_path = Path(DATA_PATH)
    file_path = data_path / filename

    assert file_path.exists()
    
    df = pd.read_excel(file_path, engine='openpyxl')
    print(df.head)    
    # Make each row into Student object

    return []


def parse_course_file(filename: str) -> List[Course]:
    """Parse a student data file `filename`

    Args:
        filename (str): the name of the file

    Returns:
        List[Course]: a list of `Course` objects
    """
    filename = filename if EXCEL_EXT in filename else filename + EXCEL_EXT
    data_path = Path(DATA_PATH)
    file_path = data_path / filename


    assert file_path.exists()
    df = pd.read_excel(file_path, engine='openpyxl')
    print(df.head)    
    # Make each row into Course object    
    
    return []
