AGE_CONDITION_BY_VAR = 25 + (72 % 10) # > 25 + (ВАРИАНТ % 10) = 27
salaryList, res, lines = [], [], []
with open("text_4_var_72", "r") as file:
    for line in file:
        line = line.split(",")
        line.pop(5)
        lines.append(line)

        salaryList.append(line[4][:-1])


averageSalary = sum([int(salary) for salary in salaryList]) / len(salaryList)

for line in lines:
    if int(line[3]) > AGE_CONDITION_BY_VAR and int(line[4][:-1]) >= averageSalary:
        res.append(line)
    else:
        line = ""

res = sorted(res, key=lambda line: line[0])

with open("result", "w") as result:
    for line in res:
        result.write(",".join(line) + "\n")