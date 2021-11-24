from typing import List, Dict
import pandas as pd
from pathlib import Path

from registration.major import Major
from registration.student import Degree, Student
from registration.course import Course, Semester

# Constants
DATA_PATH = "./data/"


def parse_course_file(filename: str, credit_filename: str, semester: Semester) -> Dict[str, Course]:
    """Parse course data file `filename` and credit_filename

    Args:
        filename (str): the name of the file

    Returns:
        Dict[str, Course]: a dictionary of `Course` objects which has 0 `num_applicants`
    """
    # Import course files
    data_path = Path(DATA_PATH)
    main_file_path = data_path / filename
    credit_file_path = data_path / credit_filename
    
    assert main_file_path.exists() and credit_file_path.exists()

    sheet_name = "2021 봄" if semester == Semester.SPRING else "2021 가을"
    main_engine = "openpyxl" if main_file_path.suffix == ".xlsx" else "xlrd"
    credit_engine = "openpyxl" if credit_file_path.suffix == ".xlsx" else "xlrd"
    
    df = pd.read_excel(main_file_path, sheet_name=sheet_name, engine=main_engine)
    credit_df = pd.read_excel(credit_file_path, engine=credit_engine)
    
    assert df.shape[0] == credit_df.shape[0]
    
    courses_dict = dict()
    
    # Make each row of df into Course object
    for _, row in df.iterrows():
        name = row["과목명"].strip()
        code = row["과목번호"].strip()
        major = Major.value_of(row["개설학과"])
        capacity = row["정원"]
        division = str(row["분반"]).strip() if not pd.isna(row["분반"]) else None
        unique_code = code + division if division else code
        is_lottery = row["추첨진행여부"] == 1
        
        course = Course(
            name, 
            unique_code, 
            major, 
            capacity,
            division, 
            is_lottery,
            semester
        )
        courses_dict[unique_code] = course

    # Fill out Course's `credit` and `is_au` using credit_df
    for _, row in credit_df.iterrows():
        code = row["과목번호"].strip()
        division = str(row["분반"]).strip() if not pd.isna(row["분반"]) else None
        unique_code = code + division if division else code
        
        credit = int(row["강:실:학"].split(":")[2].split(".")[0])
        is_au = row["AU"] > 1
        
        courses_dict[unique_code].credit = credit
        courses_dict[unique_code].is_au = is_au

    return courses_dict


def parse_student_file(filename: str, courses_dict: Dict[str, Course]) -> Dict[str, Student]:
    """
    Parse a student data file `filename` with `courses_dict`

    Args:
        filename (str): the name of the file

    Returns:
        Dict[str, Student]: a dictionary of `Student` objects
    """
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


def generate_major_enum(filename: str):
    """Generate major enums using `filename`

    Args:
        filename (str): an excel file holding course information
    """
    data_path = Path(DATA_PATH)
    file_path = data_path / filename

    assert file_path.exists()
    df = pd.read_excel(file_path, engine='openpyxl')
    
    major_dict = dict()
    for _, row in df.iterrows():
        major_dict[row["개설학과"].strip()] = row["과목번호"][:3] if row["과목번호"][2].isalpha() else row["과목번호"][:2]

    for key, value in major_dict.items():
        print(value, "=", f'"{key}"')

