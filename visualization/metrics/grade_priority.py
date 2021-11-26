import matplotlib.pyplot as plt
from registration.course import CourseType

def is_necessary(course, label):
    if label == 'Logical Writing' and course.name == "논리적글쓰기":
        return True
    if label == 'AU' and course.is_au:
        return True
    if label == 'Basic Required' and course.course_type == CourseType.BASIC_REQUIRED:
        return True
    if label == 'All' and course.is_lottery:
        return True
    return False

def grade_satisfaction(results):
    labels = ['Logical Writing', 'AU', 'Basic Required', 'All']
    for label in labels:
        plt.clf()

        for system in results:
            students = results[system]
            y = [[] for i in range(5)]
            timetables = {}
            final_timetables = {}
            for i in range(1, 6):
                timetables[i] = 0
                final_timetables[i] = 0

            for s in students:
                grade =  2022 - s.year
                if grade > 5:
                    grade = 5
                for course in s.timetable:
                    if is_necessary(course, label):
                        timetables[grade] +=1
                for course in s.final_timetable:
                    if is_necessary(course, label):
                        final_timetables[grade] +=1
            for i in range(5):
                if (timetables[i+1] == 0):
                    y[i].append(0)
                else:
                    y[i].append(final_timetables[i+1] / timetables[i+1] * 100)
            x = list(range(1, 6))
            plt.plot(x, y, label=system)
        plt.xticks(x)
        plt.xlabel("Grade")
        plt.ylabel("Win rate")
        plt.title("Grade satisfaction for "+label)
        plt.legend()
        plt.savefig('result/grade_satisfaction_'+label+'.png', dpi = 300)
