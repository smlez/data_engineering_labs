import re

with open("text_1_var_72", "r") as file:
    textFile = file.read()

textFile = re.sub(r"[.!,?]", "", textFile)

splittedText = textFile.split()

words_count = {word: splittedText.count(word) for word in splittedText}

sortedDictionary = {
    word: count
    for word, count in sorted(
        words_count.items(), key=lambda item: item[1], reverse=True
    )
}

with open("result", "w") as result:
    for key, value in sortedDictionary.items():
        result.write(f"{key} : {value}\n")