from typing import List, Dict
import pandas as pd
from pathlib import Path

from registration.major import Major
from registration.student import Degree, Student
from registration.course import Course, CourseType, Semester

# Constants
DATA_PATH = "./data/"


def parse_course_file(filename: str, credit_filename: str, semester: Semester) -> Dict[str, Course]:
    """Parse course data file `filename` and credit_filename

    Args:
        filename (str): the name of the file
        credit_filename (str): the name of the file with credits
        semester (Semester): the semester to parse

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
        course_type = CourseType.value_of(row["과목구분"])
        division = str(row["분반"]).strip() if not pd.isna(row["분반"]) else None
        unique_code = code + division if division else code
        
        credit = int(row["강:실:학"].split(":")[2].split(".")[0])
        is_au = row["AU"] > 1
        
        courses_dict[unique_code].credit = credit
        courses_dict[unique_code].is_au = is_au
        courses_dict[unique_code].course_type = course_type

    return courses_dict


def parse_student_file(filename: str, courses_dict: Dict[str, Course], semester: Semester) -> Dict[str, Student]:
    """
    Parse a student data file `filename` with `courses_dict`
    Add applicants to courses_dict
    
    Args:
        filename (str): the name of the file
        courses_dict (Dict[str, Course]): a dictionary of `Course` objects
        semester (Semester): the semester to parse

    Returns:
        Dict[str, Student]: a dictionary of `Student` objects
    """
    data_path = Path(DATA_PATH)
    file_path = data_path / filename

    assert file_path.exists()
    
    sheet_name = "2021 봄" if semester == Semester.SPRING else "2021 가을"
    engine = "openpyxl" if file_path.suffix == ".xlsx" else "xlrd"
    
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine=engine)
    students_dict = dict()
    
    for _, row in df.iterrows():
        # Find the course
        code = row["과목번호"].strip()
        unique_code = code + str(row["분반"]).strip() if not pd.isna(row["분반"]) else code
        
        assert unique_code in courses_dict.keys()
        
        course = courses_dict[unique_code]
        course.add_num_applicants()
        
        # Find the student
        id = row["가명학번"]
        if id not in students_dict.keys():
            year = int(id[:4])
            degree = Degree.value_of(row["과정"])
            major = Major.value_of(row["소속학과"])

            minor = None            
            if not pd.isna(row["부전공"]):
                minor = Major.value_of(row["부전공"])

            double_major = None
            if not pd.isna(row["복수전공"]):
                double_major = Major.value_of(row["복수전공"])
            
            timetable = [course]
            
            student = Student(
                id,
                year,
                degree,
                major,
                double_major,
                minor,
                timetable,
                []
            )
            
            students_dict[id] = student
            continue
        else:
            students_dict[id].add_to_timetable(course)

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


def generate_course_type_enum(filename: str, semester: Semester):
    """Generate course type enums using `filename` and `semester`

    Args:
        filename (str): an excel file holding course information
        semester (Semester): the semester to use
    """
    data_path = Path(DATA_PATH)
    file_path = data_path / filename

    assert file_path.exists()
    
    sheet_name = "2021 봄" if semester == Semester.SPRING else "2021 가을"
    engine = "openpyxl" if file_path.suffix == ".xlsx" else "xlrd"
    
    df = pd.read_excel(file_path, engine=engine)
    
    course_type_dict = dict()
    for _, row in df.iterrows():
        value = row["과목구분"].strip()
        if "필수" in value:
            key = "REQUIRED"
        if "선택" in value:
            key = "ELECTIVE"            
            
        if "전공" in value:
            key = "MAJOR" + "_" + key
        if  "교양" in value:
            key = "LIBERAL_ARTS" + "_" + key
        if "자유" in value:
            key = "UNRESTRICTED" + "_" + key
        if "기초" in value:
            key = "BASIC" + "_" + key
        if "공통" in value:
            key = "COMMON" + "_" + key

        if "연구" in value:
            key = "RESEARCH"
            value = "연구"
        if "세미나" in value:
            key = "SEMINAR"
            value = "세미나"
        if key == "ELECTIVE":
            key = "ELSE"
            value = "기타"

        course_type_dict[key] = value
    
    for key, value in course_type_dict.items():
        print(f'{key} = "{value}"')
