import matplotlib.pyplot as plt
from visualization.metrics.credit_distribution import credit_ratio, credit_distribution
from visualization.metrics.major_priority import major_satisfaction, major_distribution
from visualization.metrics.grade_priority import grade_satisfaction
import pandas as pd
import os

def check(results):
    print("전체 final timetable 길이가 모두 동일한지 체크")
    # grade priority만 개수가 다름. 
    for system in results:
        sum = 0
        for s in results[system]:
            sum += len(s.final_timetable)
        print(sum, system)
    
def evaluation(results, semester):
    semester = str(semester).replace('Semester.', '').lower()
    os.makedirs('./result/'+semester, exist_ok=True)

    # 학생이 신청한 학점 / 당첨된 학점 분포 표시
    credit_distribution(results, semester)

    # 학생이 신청한 학점 / 당첨된 학점 구간 별 비율을 pie chart로 표시
    credit_ratio(results, semester)

    # 전공 / 복수전공 / 부전공 / 전공X 별
    # 수강신청 대비 당첨 비율  (만족도)
    major_satisfaction(results, semester)

    # 과목별 주전/복전/부전 신청 및 당첨 비율
    # 1. 막대그래프 2. 원그래프
    major_distribution(results, semester)

    # 학년 별 수강신청 대비 당첨 비율 
    grade_satisfaction(results, semester)
