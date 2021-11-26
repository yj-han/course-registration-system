import matplotlib.pyplot as plt
from visualization.metrics.credit_distribution import credit_comparison_ratio, credit_distribution
from visualization.metrics.major_prioirty import major_distribution
from visualization.metrics.year_priority import year_distribution
import pandas as pd

def evaluation(results):
    df = pd.DataFrame(index=['wish']+list(results.keys()))
    # 학생이 신청한 학점 / 당첨된 학점 / 실제 수강한 학점 분포
    df = credit_distribution(results, df)

    # 학생이 신청한 학점 대비 당첨된 학점.
    credit_comparison_ratio(results)

    # 전공 / 복수전공 / 부전공 / 전공X 별
    # 수강신청 대비 당첨 비율  (만족도)
    major_distribution(results)

    # 과목별 주전/복전/부전 신청 및 당첨 비율

    # 학년 별 수강신청 대비 당첨 비율 
    year_distribution(results)