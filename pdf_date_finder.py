from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import datefinder
import io

class PDFDateFinder:
    def readFile(self,textFile):
            fileObj = open(textFile, "r") #opens the file in read mode
            words = fileObj.read().splitlines() #puts the file into an array
            fileObj.close()
            return words

    # function checks to see if there is a number in the string, if there is it returns true.
    def containsNumber(self,value):
        for character in value:
            if character.isdigit():
                return True
        return False

    # function will look for dates. For every date found, it will save the line, along with the date found
    # if there are multiple dates found in the same line, it will save that line as many times as there are dates found
    # for example, if the line has 3 dates, it will save that line three times, each time with a date connected to it
    def findDates(self, fileName):
        dates = []
        lines = []
        words = self.readFile(fileName)
        for word in words:
            if self.containsNumber(word):
                matches = datefinder.find_dates(word, source = True)
                for match in matches:
                    dates.append(match)
                    lines.append(word)
                    break
                
            #else:
                #print("There was no date in that line.")
        return dates, lines

    def pdf2txt(self,inPDFfile, outTXTFile):
        inFile = open(inPDFfile, 'rb')
        resMgr = PDFResourceManager()
        retData = io.StringIO()
        TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
        interpreter = PDFPageInterpreter(resMgr, TxtConverter)

        #process each page in pdf file
        for page in PDFPage.get_pages(inFile):
            interpreter.process_page(page)

        txt = retData.getvalue()
        #save output data to a text file
        with open(outTXTFile, 'w') as f:
            f.write(txt)