import sys
from reader import Reader

def main():
    reader = Reader()
    reader.display_interface(sys.argv)

if __name__ == "__main__":
    main()  