import matplotlib.pyplot as plt
from registration.student import Degree
from visualization.color import COLOR

def sum_credits(timetable):
    credits = 0
    for course in timetable:
        credits += course.credit
    return credits

def credit_distribution(results):
    plt.clf()
    plt.figure(figsize=(8,8))
    # get wish credit
    wish_credits = []
    students = results[list(results.keys())[0]]
    for s in students:
        if s.degree == Degree.BACHELOR:
            wish_credit = sum_credits(s.timetable)
            if wish_credit > 0:
                wish_credits.append(wish_credit)
    
    args = dict(alpha = 0.5, bins = int(max(wish_credits))+1)
    plt.hist(wish_credits, **args, color=COLOR.ELSE, label = "wish credits")

    # get win credit for each system
    for system in results:
        students = results[system]
        final_credits = []
        for s in students:
            if s.degree == Degree.BACHELOR:
                final_credit = sum_credits(s.final_timetable)
                wish_credit = sum_credits(s.timetable)
                if wish_credit > 0:
                    final_credits.append(final_credit)
        args = dict(alpha = 0.5, bins = int(max(final_credits))+1)
        plt.hist(final_credits, **args, color=COLOR.value_of(system), label = "win credits of "+system+" system")
        
    plt.xlim(0, int(max(credits)))
    plt.savefig('result/credit_distribution.png', dpi=300)

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
