import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from registration.student import Degree
from visualization.color import COLOR

def sum_credits(timetable):
    credits = 0
    for course in timetable:
        credits += course.credit
    return credits

def credit_distribution(results):
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

    
    bins = int(MAX_CREDIT)
    histogram, _ = np.histogram(wish_credits, bins = bins)
    plt.plot(range(bins), list(histogram[:MAX_CREDIT]), color=COLOR.ELSE, alpha = 0.5, label = "wish credits")
    
    # get win credit for each system
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

        df.loc[system, ">= 9 credits (%)"] = round(over_standard / all_students * 100, 2)
        
        bins = int(MAX_CREDIT)
        histogram, _ = np.histogram(final_credits, bins = bins)
        plt.plot(range(bins), list(histogram[:MAX_CREDIT]), color=COLOR.value_of(system), label = "win credits of "+system+" system")
        
    plt.xticks(range(bins))
    plt.xlabel("Credits of final timetable")
    plt.ylabel("# of students")
    plt.legend(loc='upper right')
    plt.savefig('result/credit_distribution.png', dpi=300)

    print(df)


## TO-DO 아직 수정 필요

def credit_comparison_ratio(results):
    # ratios = []
    # for s in students[:10]:
    #     if s.degree == Degree.BACHELOR:
    #         wish_credit = sum_credits(s.timetable)
    #         final_credit = sum_credits(s.final_timetable)
    #         if (wish_credit > 0):
    #             ratios.append(final_credit / wish_credit * 100)
    # args = dict(alpha = 0.5)
    # plt.clf()
    # plt.figure(figsize=(12,8))
    # plt.hist(ratios, **args, color="r", label = "ratios")
    # plt.legend()
    # #plt.show()
    # plt.savefig('visualization/result/credit_comparison.png', dpi=300)
    pass