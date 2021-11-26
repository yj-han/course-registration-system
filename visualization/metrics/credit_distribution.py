import matplotlib.pyplot as plt
import numpy as np
from registration.student import Degree
from visualization.color import COLOR

def sum_credits(timetable):
    credits = 0
    for course in timetable:
        credits += course.credit
    return credits

def credit_distribution(results, df):
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

    bins = int(max(wish_credits)/3)
    histogram, _ = np.histogram(wish_credits, bins = bins)
    plt.plot(range(bins), list(histogram), color=COLOR.ELSE, alpha = 0.5, label = "wish credits")
    
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

        bins = int(max(final_credits)/3)
        histogram, _ = np.histogram(final_credits, bins = bins)
        plt.plot(range(bins), list(histogram), color=COLOR.value_of(system), label = "win credits of "+system+" system")
        
    plt.xticks(range(bins), [i*3 for i in range(bins)])
    plt.xlabel("credits of final timetable")
    plt.ylabel("# of students")
    plt.legend(loc='upper right')
    plt.savefig('result/credit_distribution.png', dpi=300)

    return df

def credit_comparison_ratio(results):
    ratios = []
    for s in students[:10]:
        if s.degree == Degree.BACHELOR:
            wish_credit = sum_credits(s.timetable)
            final_credit = sum_credits(s.final_timetable)
            if (wish_credit > 0):
                ratios.append(final_credit / wish_credit * 100)
    args = dict(alpha = 0.5)
    plt.clf()
    plt.figure(figsize=(12,8))
    plt.hist(ratios, **args, color="r", label = "ratios")
    plt.legend()
    #plt.show()
    plt.savefig('visualization/result/credit_comparison.png', dpi=300)
