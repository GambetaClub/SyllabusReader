import sys
from pdf2txt import pdf2txt
from pdfDateFinder import findDates

from ICSConverter import ICSConverter
from Reader import Reader

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    
    #reading docx file
    reader = Reader(sys.argv[1])

    reader.load_syllabi()
    syllabi = reader.get_syllabi()
    for syllabus in syllabi:
        syllabi[syllabus].to_csv(f"{syllabus}.csv", index=False)

    #creating a ics file from csv files
    converter = ICSConverter(sys.argv[1])

    converter.readCSV(f"Syllabus1.csv")
    converter.readCSV(f"Syllabus2.csv")

    converter.exportICS()

    #reading a pdf
    inPDFfile = 'syllabus1.pdf'
    outTXTFile = 'syllabus1.txt'
    pdf2txt(inPDFfile, outTXTFile)
    print("pdf to text finish")

    findDatesTuple = findDates("syllabus1.txt")
    print("find dates finished")
    dates = findDatesTuple[0]
    lines = findDatesTuple[1]
    for date, line in zip(dates, lines):
        print(line, date)

if __name__ == "__main__":
    main()  