from numpy.lib import index_tricks
import pandas as pd
from classes.student import Student, Degree
from classes.course import Course
from classes.major import Major
import pickle

student_path = "../data/wishlist.xlsx"
course_path = "../data/course_update.xlsx"

pickle_course_path = "../data/course.pickle"
pickle_student_path = "../data/student.pickle"

def read_course_info():
    df = pd.ExcelFile(course_path).parse(
        sheet_name=0,        
        usecols=range(13),   
        engine='xlrd',       
        verbose=True)        
    courses = []
    for i in range(len(df)):
        c = df.iloc[i]
        name = c['과목명']
        major = Major.value_of(c['개설학과'])
        code = c['전산코드']
        division = c['분반']
        capacity = c['정원']
        num_applicants = c['실제수강인원']
        is_lottery = c['추첨진행여부']
        au = c['AU']
        credit = c['학점']
        classification = c['과목구분']
        course = Course(
            name, code, major, classification, credit, capacity, 
            division, num_applicants, is_lottery, au)
        courses.append(course)
    
    with open(pickle_course_path, 'wb') as f:
        pickle.dump(courses, f)

def read_student_info():
    with open(pickle_course_path, 'rb') as f:
        courses = pickle.load(f)

    df = pd.ExcelFile(student_path).parse(
        sheet_name=0,        
        usecols=range(14),   
        engine='xlrd',       
        verbose=True)         
    students = []

    for i in range(len(df)):
        s = df.iloc[i]
        id = s['가명학번']
        year = int(id[:4])
        degree = Degree.value_of(s['과정'])
        major = Major.value_of(s['소속학과'])
        minor = Major.value_of(str(s['부전공']))
        double_major = Major.value_of(str(s['복수전공']))
        final = s['최종수강여부']
        win = s['당첨여부']

        index_of_course = -1
        for j in range(len(courses)):
            if (courses[j].code == s['전산코드'] and
                courses[j].division == s['분반']):
                index_of_course = j
                break

        contain = False
        for j in range(len(students)):
            if id == students[j].id:
                students[j].add_to_timetable(index_of_course)
                if final == 1:
                    students[j].add_to_final_timetable(index_of_course)
                if win != 0:
                    students[j].add_to_win_timetable(index_of_course)
                contain = True
                break
        if not contain:
            win_course = []
            final_course = []
            if final == 1:
                final_course = [index_of_course]
            if win != 0:
                win_course = [index_of_course]
            student = Student(id, year, degree, major, minor, double_major,
                [index_of_course], win_course, final_course)
            students.append(student)
    with open(pickle_student_path, 'wb') as f:
        pickle.dump(students, f)

read_course_info()
# read_student_info()