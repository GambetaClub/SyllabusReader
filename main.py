import sys

from ics_converter import ICSConverter
from reader import Reader

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == "true" or sys.argv[1].lower() == "true":
            print("eso")
    #reading docx file
    reader = Reader(sys.argv[1])

    reader.load_syllabi()
    syllabi = reader.get_syllabi()

    #creating a ics file from csv files
    converter = ICSConverter(sys.argv[1])
    for syllabus in syllabi:
        syllabi[syllabus].to_csv(f"{syllabus}.csv", index=False)
        converter.readCSV(f"{syllabus}.csv")

    converter.exportICS()

if __name__ == "__main__":
    main()  