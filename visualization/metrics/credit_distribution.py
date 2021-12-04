import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from registration.student import Degree
from visualization.color import COLOR
from visualization.marker import MARKER

def sum_credits(timetable):
    credits = 0
    for course in timetable:
        credits += course.credit
    return credits

def credit_distribution(results, semester):
    # save the value % of students who finally get over 9 credits
    df = pd.DataFrame(index=['wish']+list(results.keys()))
    # maximum credit that is shown in the graph
    MAX_CREDIT = 25

    plt.clf()
    plt.figure(figsize=(8,8))
    # get wish credit
    system = list(results.keys())[0]
    wish_credits = []
    students = results[system]

    all_students = 0
    over_standard = 0
    for s in students:
        if s.degree == Degree.BACHELOR:
            all_students += 1
            wish_credit = sum_credits(s.timetable)
            if wish_credit > 0:
                wish_credits.append(wish_credit)
            if wish_credit > 9:
                over_standard += 1
    
    df.loc['wish', ">= 9 credits (%)"] = round(over_standard / all_students * 100, 2)

    bins = int(max(wish_credits))
    histogram, _ = np.histogram(wish_credits, bins = bins)
    plt.plot(range(MAX_CREDIT), list(histogram[:MAX_CREDIT]), color=COLOR.ELSE, alpha = 0.5, label = "wish credits")
    
    # get win credit for each system

    systems = list(results.keys())
    systems.remove('grade priority')
    systems.remove('major priority')

    for system in systems:
        final_credits = []
        students = results[system]
        over_standard = 0
        for s in students:
            if s.degree == Degree.BACHELOR:
                final_credit = sum_credits(s.final_timetable)
                wish_credit = sum_credits(s.timetable)
                if wish_credit > 0:
                    final_credits.append(final_credit)
                if final_credit > 9:
                    over_standard += 1

        df.loc[system, ">= 9 credits (%)"] = round(over_standard / all_students * 100, 2)
        
        bins = int(max(wish_credits))
        histogram, _ = np.histogram(final_credits, bins = bins)
        plt.plot(range(MAX_CREDIT), list(histogram[:MAX_CREDIT]), color=COLOR.value_of(system), marker=MARKER.value_of(system), label = "win credits of "+system+" system")
        
    plt.xticks(range(MAX_CREDIT))
    plt.xlabel("Credits of final timetable")
    plt.ylabel("# of students")
    plt.legend(loc='upper right')
    plt.savefig('result/'+semester+'/credit_distribution.png', dpi=300)
    plt.close()
    print(df)

def credit_ratio(results, semester):

    plt.clf()
    plt.figure(figsize=(8,12))
    # get wish credit
    system = list(results.keys())[0]
    wish_credits = []
    students = results[system]

    all_students = 0
    over_standard = 0
    for s in students:
        if s.degree == Degree.BACHELOR:
            all_students += 1
            wish_credit = sum_credits(s.timetable)
            if wish_credit > 0:
                wish_credits.append(wish_credit)
            if wish_credit > 9:
                over_standard += 1
      
    bins = int(max(wish_credits))
    histogram, _ = np.histogram(wish_credits, bins = bins)
    
    labels = ['0~8 credits', '9~14 credits', '15~20 credits', '21~ credits']
    colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0']
    
    ratio = [sum(histogram[:9]), sum(histogram[9:15]), sum (histogram[15:21]), sum(histogram[21:])]
    plt.subplot(321)
    pie = plt.pie(ratio, labels=labels, counterclock=False, colors=colors, autopct='%.2f%%', startangle=180)
    plt.title("Wish credits")
    # get win credit for each system
    i=0
    for system in results:
        final_credits = []
        students = results[system]
        over_standard = 0
        for s in students:
            if s.degree == Degree.BACHELOR:
                final_credit = sum_credits(s.final_timetable)
                wish_credit = sum_credits(s.timetable)
                if wish_credit > 0:
                    final_credits.append(final_credit)
                if final_credit > 9:
                    over_standard += 1

        bins = int(max(wish_credits))
        histogram, _ = np.histogram(final_credits, bins = bins)
        plt.subplot(322 + i)
        i+=1
        ratio = [sum(histogram[:9]), sum(histogram[9:15]), sum (histogram[15:21]), sum(histogram[21:])]
        plt.pie(ratio, counterclock=False, labels=labels, colors=colors, autopct='%.2f%%', startangle=180)        
        plt.title("Final credits for "+ system + " system")
    plt.subplot(326)
    plt.axis("off")
    plt.legend(pie[0], labels, loc="center")
    plt.savefig('result/'+semester+'/credit_distribution_pie.png', dpi=300)
    plt.close()