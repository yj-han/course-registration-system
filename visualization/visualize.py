import pickle
import matplotlib.pyplot as plt
import numpy
from classes.major import Major
from classes.student import Degree

major_list = set()
pickle_student_path = "data/student.pickle"
pickle_course_path = "data/course.pickle"

with open(pickle_course_path, 'rb') as f:
        courses = pickle.load(f)

with open(pickle_student_path, 'rb') as f:
        students = pickle.load(f)

def sum_credits(timetable):
    credits = 0
    for t in timetable:
        if t != -1:
            credits += courses[t].credit
    return credits

def credit_compare():
    credits = []
    win_credits = []
    final_credits = []
    for s in students:
        if s.degree == Degree.BACHELOR:
            credits.append(sum_credits(s.timetable))
            win_credits.append(sum_credits(s.win_timetable))
            final_credits.append(sum_credits(s.final_timetable))
    
    args = dict(alpha = 0.5, bins = 100)
    plt.clf()
    plt.figure(figsize=(12,8))
    plt.hist(win_credits, **args, color="b", label = "win credits")
    plt.hist(final_credits, **args, color="r", label = "final credits")
    plt.hist(credits, **args, color="g", label = "wish credits")
    plt.xlim(0, 24)
    plt.legend()
    # plt.show()
    plt.savefig('visualization/result/credit_comparison.png', dpi=300)

def applicants_ratio():
    args = dict(alpha = 0.5, bins = 100)

    ratios = []
    for c in courses:
        if c.capacity != 0:
            ratios.append(c.num_applicants / c.capacity)
    plt.clf()   
    plt.figure(figsize=(12,8)) 
    plt.hist(ratios, **args, color="g", label = "# of applicants / capacity")
    plt.legend()
    # plt.show()
    plt.savefig('visualization/result/applicants_capacity_ratio.png', dpi=300)

def get_major_list():
    for c in courses:
        major_list.add(c.major)
    for s in students:
        major_list.add(s.major)

def timetable_per_major(s, timetable, timetables):
    for t in timetable:   
        if t == -1 or not courses[t].is_lottery:
            continue
        major = courses[t].major
        if s.major == major:
            timetables[major]['major'] += 1
        elif s.minor == major:
            timetables[major]['minor'] += 1
        elif s.double_major == major:
            timetables[major]['double_major'] += 1
        else:
            timetables[major]['no_major'] += 1
        timetables[s.major]['all'] += 1
    return timetables

def get_ratios(timetables, win_timetables, label, major):
    ratio = []
    for t in label:
        if timetables[t][major] != 0:
            value = win_timetables[t][major] / timetables[t][major]*100
            ratio.append(value)
        else:
            ratio.append(0)
    return ratio

def avg(L):
    return round(sum(L)/len(L), 2)

def major_distribution():
    timetables = {}
    win_timetables = {}
  
    for m in major_list:
        timetables[m] = {'major': 0, 'minor':0, 'double_major':0, 'no_major':0, 'all':0}
        win_timetables[m] = {'major': 0, 'minor':0, 'double_major':0, 'no_major':0, 'all':0}
    
    for s in students:
        if s.degree == Degree.BACHELOR:
            timetables = timetable_per_major(s, s.timetable, timetables)
            win_timetables = timetable_per_major(s, s.win_timetable, win_timetables)

    # all list of major
    label = list(major_list)

    # 학부생 major
    label = [Major.MAS, Major.PH, Major.CH, Major.BS,
        Major.BiS, Major.IE, Major.ID, Major.NQE,
        Major.MS, Major.CS, Major.EE, Major.CE,
        Major.CBE, Major.MSB, Major.ME, Major.AE,
        Major.FRESH]

    x = numpy.arange(len(label))
    majors = get_ratios(timetables, win_timetables, label,"major")
    minors = get_ratios(timetables, win_timetables, label,"minor")
    double_majors = get_ratios(timetables, win_timetables, label,"double_major")
    no_majors = get_ratios(timetables, win_timetables, label,"no_major")


    print("majors",avg(majors), 
        "minors", avg(minors), 
        "double majors", avg(double_majors), 
        "no majors", avg(no_majors))
    
    plt.clf()
    plt.figure(figsize=(16,8))
    plt.bar(x, majors, label="major", width=0.1)
    plt.bar(x+0.1, double_majors, label="double major", width=0.1)
    plt.bar(x+0.2, minors, label="minor", width=0.1)
    plt.bar(x+0.3, no_majors, label="non major", width=0.1)
    plt.xticks(x+0.15, label)
    plt.ylim(0, 100)
    plt.ylabel("% of winning for lottery courses")

    plt.legend()
    # plt.show()
    plt.savefig('visualization/result/winning_percent_for_lottery.png', dpi=300)

def is_necessary(t, label):
    course = courses[t]
    if label == 'Logical Writing' and course.name == "논리적글쓰기":
        return True
    if label == 'AU' and course.au > 0:
        return True
    if label == 'Basic Required' and course.classification == "기초필수":
        return True
    if label == 'lottery' and course.is_lottery:
        return True
    return False

def year_distribution():
    labels = ['Logical Writing', 'AU', 'Basic Required', 'lottery']
    ratio_results = [[] for i in range(5)]
    for j in range(len(labels)):
        label = labels[j]
        timetables = {}
        win_timetables = {}
        for i in range(1, 6):
            timetables[i] = 0
            win_timetables[i] = 0

        for s in students:
            year =  2022 - int(s.year)
            if (year>5):
                year = 5
            for t in s.timetable:
                if is_necessary(t, label):
                    timetables[year] +=1
            for t in s.win_timetable:
                if is_necessary(t, label):
                    win_timetables[year] +=1
        for i in range(1, 6):
            if (timetables[i] == 0):
                ratio_results[i-1].append(0)
            else:
                ratio_results[i-1].append(win_timetables[i] / timetables[i] * 100)
    
    x = numpy.arange(len(labels))
    plt.clf()
    plt.figure(figsize=(12,8))
    for i in range(5):
        plt.bar(x+i/10, ratio_results[i], label=str(i+1), width=0.1)
    plt.xticks(x+0.25, labels)
    plt.savefig('visualization/result/ratio_per_years.png', dpi=300)
    pass

# 학생이 신청한 학점/당첨된 학점/실제 수강한 학점 분포
credit_compare()

# 수업별 정원의 비율 분포
applicants_ratio()

# 전공 / 복수전공 / 부전공 / 전공X 별
# 수강신청 대비 당첨 비율  (만족도)
get_major_list()
major_distribution()

# TO-DO
# 과목별 주전/복전/부전 신청 및 당첨 비율

# 학년 별 수강신청 대비 당첨 비율 
year_distribution()
