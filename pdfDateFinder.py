from logging import NullHandler
import datefinder
from regex.regex import Match

def readFile(textFile):
        fileObj = open(textFile, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

# function checks to see if there is a number in the string, if there is it returns true.
def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

# function will look for dates. For every date found, it will save the line, along with the date found
# if there are multiple dates found in the same line, it will save that line as many times as there are dates found
# for example, if the line has 3 dates, it will save that line three times, each time with a date connected to it
def findDates(fileName):
    dates = []
    lines = []
    words = readFile(fileName)
    for word in words:
        if containsNumber(word):
            matches = datefinder.find_dates(word, source = True)
            for match in matches:
                dates.append(match)
                lines.append(word)
        else:
            print("There was no date in that line.")
    return dates, lines