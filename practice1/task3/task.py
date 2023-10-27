result = []
VAR_CONDITION = 50 + 72 # 50 + вариант

with open("text_3_var_72", "r") as file:
    for line in file:
        line = line.strip("\n").split(",")

        for i in range(len(line)):
            if line[i] == "NA":
                line[i] = str(int((int(line[i - 1]) + int(line[i + 1])) / 2))

        line = list(filter(lambda num: int(num) ** 0.5 >= VAR_CONDITION, line))

        if line != []:
            result.append(line)
print(result)
with open("result", "w") as res:
    for res in result:
        res.write(",".join(res) + "\n")