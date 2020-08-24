import re
def readTickers(exchangeFilePath):
    file_path = exchangeFilePath
    lines = open(file_path,'r').readlines()
    for l in lines[1:]:
        if re.split(r' \t+', l)[0] not in currencyPairs:
            currencyPairs.append(re.split(r' \t+', l)[0])

currencyPairs = []

readTickers("Currency_Pairs.txt")


fileName = "currency_pairs_clean.txt"
text_file = open(fileName, "w")
for cp in currencyPairs:
    text_file.write(str(cp)+ "\n")
text_file.close()