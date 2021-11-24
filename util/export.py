import pickle


# Constants
DATA_PATH = "./data/"
EXCEL_EXT = ".xlsx"


def export_students(students):
    """
    Export students to a pickle file
    """
    with open(DATA_PATH + "students.pkl", "wb") as f:
        pickle.dump(students, f)


def export_courses(courses):
    """
    Export courses to a pickle file
    """
    with open(DATA_PATH + "courses.pkl", "wb") as f:
        pickle.dump(courses, f)
