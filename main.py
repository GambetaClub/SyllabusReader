import sys
from reader import Reader


def main():
    reader = Reader()
    # if len(sys.argv) < 2:
    #     sys.exit("Usage: python3 main.py <directory_name>")
    # reader.set_directory(sys.argv[1])
    reader.load_syllabi()
    reader.display_interface(sys.argv)

if __name__ == "__main__":
    main()  