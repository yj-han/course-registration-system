
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

def major_distribution(students, courses):
    timetables = {}
    win_timetables = {}
  
    major_list = get_major_list()

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
    plt.savefig('visualization/result/winning_percent_for_lottery.png', dpi=300)

