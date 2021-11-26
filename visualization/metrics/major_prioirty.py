import matplotlib.pyplot as plt
import numpy as np
from registration.student import Degree
from registration.major import Major
from visualization.color import COLOR

majors = [Major.CS, Major.EE, Major.ID, Major.MAS]
def timetable_per_major(s, timetable, timetables):
    for course in timetable:   
        if not course.is_lottery:
            continue
        major = course.major
        if major not in majors:
            continue

        if s.major == major:
            major_type = 'major'
        elif s.minor == major:
            major_type = 'minor'
        elif s.double_major == major:
            major_type = 'double_major'
        else:
            major_type = 'no_major'

        if major in timetables:
            timetables[major][major_type] += 1
            timetables[major]['all'] += 1
        else:
            timetables[major] = {'all': 1, 'major':0, 'minor':0, 'double_major':0, 'no_major':0}
            timetables[major][major_type] += 1
    return timetables

def avg(L):
    return round(sum(L)/len(L), 2)

def get_ratios(timetables, final_timetables, major):
    ratio = {}
    for major_type in timetables[major]:
        try:
            value = final_timetables[major][major_type] / timetables[major][major_type]*100
            ratio[major_type] = value
        except:
            ratio[major_type] = float(0)
    return ratio

def get_major_ratios(major_satisfaction, major_type):
    ratios = []
    systems = list(major_satisfaction.keys())
    for system in systems:
        ratios.append(major_satisfaction[system][major_type])
    return ratios

def major_satisfaction(results):
    major_satisfaction = {}
    systems = list(results.keys())
    for system in systems:
        timetables = {}
        final_timetables = {}
        students = results[system]
        for s in students:
            timetables = timetable_per_major(s, s.timetable, timetables)
            final_timetables = timetable_per_major(s, s.final_timetable, final_timetables)

        for major in majors:
            ratios = get_ratios(timetables, final_timetables, major)
            try:
                major_satisfaction[major][system] = ratios
            except:
                major_satisfaction[major] = {system : ratios}
    
    ## 각 전공 별 주전/복전/부전 각각의 만족도 그래프
    for major in majors:
        x = np.arange(len(systems))
        plt.clf()
        plt.figure(figsize=(16,8))

        plt.bar(x, get_major_ratios(major_satisfaction[major], "major"), label="major", width=0.1)
        plt.bar(x+0.1, get_major_ratios(major_satisfaction[major], "double_major"), label="double major", width=0.1)
        plt.bar(x+0.2, get_major_ratios(major_satisfaction[major], "minor"), label="minor", width=0.1)
        plt.bar(x+0.3, get_major_ratios(major_satisfaction[major], "no_major"), label="non major", width=0.1)
        
        plt.xticks(x+0.15, systems)
        plt.ylim(0, 100)
        plt.ylabel("Win rate")
        plt.xlabel("Systems")
        major_name = str(major).removeprefix('Major.')
        plt.title("Major satisfaction for "+major_name+" major")
        plt.legend()
        plt.savefig('result/major_satisfaction_'+major_name+'_major.png', dpi=300)