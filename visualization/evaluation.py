import matplotlib.pyplot as plt
from visualization.metrics.credit_distribution import credit_comparison_ratio, credit_distribution
from visualization.metrics.major_prioirty import major_satisfaction, major_distribution
from visualization.metrics.grade_priority import grade_distribution
import pandas as pd

def check(results):
    print("전체 final timetable 길이가 모두 동일한지 체크")
    # grade priority만 개수가 다름. 
    for system in results:
        sum = 0
        for s in results[system]:
            sum += len(s.final_timetable)
        print(sum, system)
    
def evaluation(results):       
    # 학생이 신청한 학점 / 당첨된 학점 / 실제 수강한 학점 분포
    credit_distribution(results)

    # TO-DO : 학생이 신청한 학점 대비 당첨된 학점.
    # credit_comparison_ratio(results)

    # 전공 / 복수전공 / 부전공 / 전공X 별
    # 수강신청 대비 당첨 비율  (만족도)
    major_satisfaction(results)

    # 과목별 주전/복전/부전 신청 및 당첨 비율
    major_distribution(results)

    # # 학년 별 수강신청 대비 당첨 비율 
    grade_distribution(results)
