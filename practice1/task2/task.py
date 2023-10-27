result = []

with open("text_2_var_72", "r") as file:
    for line in file:
        splittedLine = line.strip("\n").split("/")
        result.append(sum([int(num) for num in splittedLine]))

with open("result", "w") as res:
    for number in result:
        res.write(str(number) + "\n")