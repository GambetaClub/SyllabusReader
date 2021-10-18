import sys
from reader import Reader

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    reader = Reader(sys.argv[1])

    reader.load_syllabi()
    syllabi = reader.get_syllabi()
    for syllabus in syllabi:
        syllabi[syllabus].to_csv(f"{syllabus}.csv", index=False)

if __name__ == "__main__":
    main()  