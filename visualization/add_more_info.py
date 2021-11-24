## 원래 excel sheet에서 AU, credit 정보 추가하기

from os import error
import pandas as pd
import numpy as np

course_path = "data/course.xlsx"
all_course_path = "data/all_courses.xls"

new_course_path = "data/course_update.xlsx"

df_to = pd.read_excel(course_path)
df_from = pd.read_excel(all_course_path,
    header = 1
)
df_from['AU'] = df_from['AU'].apply(lambda x: int(x))
df_from['학점'] = df_from['강:실:학'].apply(lambda x: float(x[-3:]))

more = ['AU', '학점', '과목구분']
df_to[more] = ""
for i in range(len(df_to)):
    index = df_from.index[df_from['전산코드'] == df_to.iloc[i]['전산코드']].to_list()
    try:
        for j in range(len(index)):
            j_index = index[j]
            fro = df_from.iloc[j_index]
            to = df_to.iloc[i+j]
            for addition in more:
                to[addition] = fro[addition]
            df_to.iloc[i+j] = to
        i+=len(index)
    except:
        print(error)
with pd.ExcelWriter(new_course_path) as writer:
    df_to.to_excel(writer, index=False)