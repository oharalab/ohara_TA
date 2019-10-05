"""
import pandas as pd

data_frame = pd.read_csv("student.csv", encoding="cp932", skiprows=2)
print(data_frame.columns)
print(data_frame["(学生番号/教職員番号)"])
print(data_frame["(氏名)"])

with open("student_temp.txt", "w") as f:
    for number, name in zip(data_frame["(学生番号/教職員番号)"], data_frame["(氏名)"]):
        f.write(str(number) + " " + name + "\n")
"""

with open("student.csv", "r", encoding = "cp932") as fr:
    # skip rows
    for i in range(3):
        fr.readline()
    with open("students.txt", "w") as fw:
        for line in fr:
            student_info = line.split(",")
            fw.write(str(student_info[3]) + " " + student_info[4] + "\n")
    

