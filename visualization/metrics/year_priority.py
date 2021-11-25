import matplotlib.pyplot as plt

def is_necessary(course, label):
    if label == 'Logical Writing' and course.name == "논리적글쓰기":
        return True
    if label == 'AU' and course.au > 0:
        return True
    if label == 'Basic Required' and course.classification == "기초필수":
        return True
    if label == 'lottery' and course.is_lottery:
        return True
    return False

def year_distribution(students, courses):
    labels = ['Logical Writing', 'AU', 'Basic Required', 'lottery']
    
    for j in range(len(labels)):
        y = [[] for i in range(5)]
        label = labels[j]
        timetables = {}
        win_timetables = {}
        for i in range(1, 6):
            timetables[i] = 0
            win_timetables[i] = 0

        for s in students:
            year =  2022 - int(s.year)
            if year > 5:
                year = 5
            for t in s.timetable:
                if is_necessary(courses[t], label):
                    timetables[year] +=1
            for t in s.win_timetable:
                if is_necessary(courses[t], label):
                    win_timetables[year] +=1
        for i in range(1, 6):
            if (timetables[i] == 0):
                y[i-1].append(0)
            else:
                y[i-1].append(win_timetables[i] / timetables[i] * 100)
        x = list(range(1, 6))
        plt.clf()
        plt.plot(x, y)
        plt.xlim([1, 5])
        plt.ylim([0, 100])
        plt.xlabel("year")
        plt.ylabel("# of Win / # of Wish")
        plt.title("Win rate for different year")
        plt.savefig('visualization/result/win_rate_for_year_'+label+'.png', dpi = 300)
