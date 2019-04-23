import pandas as pd

data_frame = pd.read_csv("student.csv", encoding="cp932", skiprows=2)
print(data_frame.columns)
print(data_frame["(学生番号/教職員番号)"])
print(data_frame["(氏名)"])

with open("student_temp.txt", "w") as f:
    for number, name in zip(data_frame["(学生番号/教職員番号)"], data_frame["(氏名)"]):
        f.write(str(number) + " " + name + "\n")

