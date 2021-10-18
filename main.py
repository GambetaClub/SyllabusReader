import sys
from pdf_date_finder import PDFDateFinder

from ics_converter import ICSConverter
from reader import Reader

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
    pdf_date_finder = PDFDateFinder()
    pdf_date_finder.pdf2txt('syllabus1.pdf', 'syllabus1.txt')
    
    findDatesTuple = pdf_date_finder.findDates("syllabus1.txt")
    print("find dates finished")
    dates = findDatesTuple[0]
    lines = findDatesTuple[1]
    for date, line in zip(dates, lines):
        print(line, date)

if __name__ == "__main__":
    main()  