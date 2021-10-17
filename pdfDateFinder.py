import datefinder
from regex.regex import Match

def readFile(textFile):
        fileObj = open(textFile, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

def findDates(fileName):
    dates = []
    words = readFile(fileName)
    for word in words:
        matches = datefinder.find_dates(word)
        for match in matches:
            dates.append(match)

    return dates