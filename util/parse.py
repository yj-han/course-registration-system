from typing import List, Dict
import pandas as pd
from pathlib import Path

from registration.major import Major
from registration.student import Degree, Student
from registration.course import Course

# Constants
DATA_PATH = "./data/"
EXCEL_EXT = ".xlsx"


def parse_student_file(filename: str, courses_dict: Dict[str, Course]) -> Dict[str, Student]:
    """
    Parse a student data file `filename` with `courses`

    Args:
        filename (str): the name of the file

    Returns:
        Dict[str, Student]: a dictionary of `Student` objects
    """
    filename = filename if EXCEL_EXT in filename else filename + EXCEL_EXT
    data_path = Path(DATA_PATH)
    file_path = data_path / filename

    assert file_path.exists()
    
    df = pd.read_excel(file_path, engine='openpyxl')
    students_dict = dict()

    for _, row in df.iterrows():
        id = row["가명학번"]
        courses_dict[row["과목번호"]].num_applicants += 1
        course = courses_dict[row["과목번호"]]

        if id not in students_dict.keys():
            year = int(id[:4])
            degree = Degree.value_of(row["과정"])
            major = Major.value_of(row["소속학과"])
            
            if not pd.isna(row["부전공"]):
                minor = Major.value_of(row["부전공"])
                double_major = None
            elif not pd.isna(row["복수전공"]):
                double_major = Major.value_of(row["복수전공"])
                minor = None
            else:
                minor = None
                double_major = None

            timetable = [course]
            final_timetable = []
            
            student = Student(id, year, degree, major, double_major, minor, timetable, final_timetable)
            students_dict[id] = student
            continue
        else:
            students_dict[id].timetable.append(course)
        
    return students_dict


def parse_course_file(filename: str) -> Dict[str, Course]:
    """Parse a student data file `filename`

    Args:
        filename (str): the name of the file

    Returns:
        Dict[str, Course]: a dictionary of `Course` objects which has 0 `num_applicants`
    """
    filename = filename if EXCEL_EXT in filename else filename + EXCEL_EXT
    data_path = Path(DATA_PATH)
    file_path = data_path / filename

    assert file_path.exists()
    df = pd.read_excel(file_path, engine='openpyxl')
    
    courses_dict = dict()
    
    # Make each row into Course object
    for _, row in df.iterrows():
        code = row["과목번호"]
        major = Major.value_of(row["개설학과"])
        credit = 1 if "URP" in code else 3
        division = str(row["분반"]) if not pd.isna(row["분반"]) else None
        is_lottery = row["추첨진행여부"] == 1
        course = Course(row["과목명"], code, major, credit, row["정원"], division, 0, is_lottery, False)
        courses_dict[code] = course
    
    return courses_dict


def generate_major_enum(filename: str):
    """Generate major enums using `filename`

    Args:
        filename (str): an excel file holding course information
    """
    filename = filename if EXCEL_EXT in filename else filename + EXCEL_EXT
    data_path = Path(DATA_PATH)
    file_path = data_path / filename

    assert file_path.exists()
    df = pd.read_excel(file_path, engine='openpyxl')
    
    major_dict = dict()
    for _, row in df.iterrows():
        major_dict[row["개설학과"].strip()] = row["과목번호"][:3] if row["과목번호"][2].isalpha() else row["과목번호"][:2]

    for key, value in major_dict.items():
        print(value, "=", f'"{key}"')

