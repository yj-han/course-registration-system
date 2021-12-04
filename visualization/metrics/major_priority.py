import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from registration.student import Degree
from registration.major import Major
from visualization.color import COLOR
from registration.course import CourseType

majors = [Major.CS, Major.EE, Major.ID]
remove_system = []

def timetable_per_major(s, timetable, timetables):
    for course in timetable:   
        if not course.is_lottery:
            continue
        if not (course.course_type == CourseType.MAJOR_REQUIRED or course.course_type == CourseType.MAJOR_ELECTIVE):
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

def major_satisfaction(results, semester):
    major_satisfaction = {}
    systems = list(results.keys())
    for s in remove_system:
        systems.remove(s)
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
    
    satisfaction_bar(major_satisfaction, semester, systems)
    satisfaction_plot(major_satisfaction, semester, systems)

def satisfaction_bar(major_satisfaction, semester, systems):
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
        major_name = str(major).replace('Major.', '')
        plt.title("Major satisfaction for "+major_name+" major")
        plt.legend()
        plt.savefig('result/'+semester+'/major_satisfaction_bar_'+major_name+'_major.png', dpi=300)
        plt.close()

def satisfaction_plot(major_satisfaction, semester, systems):
    for major in majors:
        plt.clf()
        for system in systems:
            x = ['major', 'double_major', 'minor', 'no_major']
            y = []
            for i in x:
                y.append(major_satisfaction[major][system][i])

            plt.plot(x, y, label=system, color=COLOR.value_of(system))
        
        plt.xticks(x)
        plt.ylabel("Win rate")
        plt.xlabel("Systems")
        major_name = str(major).replace('Major.', '')
        plt.title("Major satisfaction for "+major_name+" major")
        plt.legend()
        plt.savefig('result/'+semester+'/major_satisfaction_plot_'+major_name+'_major.png', dpi=300)
        plt.close()

def major_distribution(results, semester):
    systems = list(results.keys())
    for s in remove_system:
        systems.remove(s)
    wish = {}
    final = {}
    for major in majors:
        wish[major] = pd.DataFrame(columns=['system','major', 'double_major', 'minor', 'no_major'])
        final[major] = pd.DataFrame(columns=['system','major', 'double_major', 'minor', 'no_major'])
    for system in systems:
        timetables = {}
        final_timetables = {}
        students = results[system]
        for s in students:
            timetables = timetable_per_major(s, s.timetable, timetables)
            final_timetables = timetable_per_major(s, s.final_timetable, final_timetables)
        for major in majors:
            timetables[major]['system'] = 'wish'
            final_timetables[major]['system'] = system
            if final[major].empty:
                final[major] = final[major].append(timetables[major], ignore_index=True)
            final[major] = final[major].append(final_timetables[major], ignore_index=True)

    bar_graph(final, systems, semester)
    pie_graph(final, systems, semester)

def bar_graph(final, systems, semester):
    ## 각 전공 별 주전/복전/부전 각각의 만족도 그래프
    for major in majors:
        x = np.arange(len(systems)+1)
        plt.clf()
        plt.figure(figsize=(16,8))
        plt.grid(True, axis='y')

        df = final[major]
        plt.bar(x, df['major'], color = 'r', width=0.2, label='major')
        plt.bar(x, df['double_major'],  bottom = df['major'], color = 'g', width=0.2, label='double major')
        plt.bar(x, df['minor'], bottom = df['major']+df['double_major'], color = 'b', width=0.2, label='minor')
        plt.bar(x, df['no_major'], bottom =  df['major']+df['double_major']+df['minor'], color = 'c', width=0.2, label='non major')

        plt.xticks(x, ['wish']+systems)
        plt.xlabel('System', fontsize = 12)
        plt.ylabel('# of students', fontsize = 12)
        major_name = str(major).replace('Major.', '')
        plt.legend()
        plt.title("Major distribution for "+major_name+" major", fontsize = 15)
        plt.savefig('result/'+semester+'/major_distribution_'+major_name+'_major.png', dpi=300)

def major_satisfaction2(results, semester):
    major_satisfaction_dict = {}
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
                major_satisfaction_dict[major][system] = ratios
            except:
                major_satisfaction_dict[major] = {system : ratios}

    ## 각 전공 별 주전/복전/부전 각각의 만족도 그래프
    for major in majors:
        plt.clf()

        for system in systems:
            students = results[system]
            x = ['major', 'double_major', 'minor', 'no_major']
            y = []
            for i in x:
                y.append(major_satisfaction_dict[major][system][i])

            plt.plot(x, y, label=system, color=COLOR.value_of(system))
        
        plt.xticks(x)
        plt.ylim(0, 100)
        plt.ylabel("Win rate")
        plt.xlabel("Systems")
        major_name = str(major).replace('Major.', '')
        plt.title("Major satisfaction for "+major_name+" major")
        plt.legend()
        plt.savefig('result/'+semester+'/major_satisfaction_plot_'+major_name+'_major.png', dpi=300)
        plt.close()

def pie_graph(final, systems, semester):
    colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0']
    for major in majors:
        i=0
        df = final[major]
        df = df.set_index('system')
        plt.clf()
        plt.figure(figsize=(8,12))
        labels = list(df.columns[:-1])
        for system in ['wish']+systems:
            ratio = list(df.loc[system])[:-1]
            plt.subplot(421+i)
            pie = plt.pie(ratio, labels = labels, counterclock = False, colors = colors, autopct='%.2f%%', startangle=180)
            i+=1
            if (system == 'wish'):
                plt.title("Wish List")
            else:
                plt.title(system.capitalize()+ " system")
        major_name = str(major).replace('Major.', '')
        plt.suptitle('Major distribution for '+major_name+' major')
        plt.savefig('result/'+semester+'/major_distribution_pie_'+major_name+"_major.png", dpi = 300)
        plt.close()
