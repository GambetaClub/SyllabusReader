import sys
import os
from pathlib import Path
import docx2txt

class Reader:
    def __init__(self, directory, files=None, calendar=None):
        self.__directory = directory
        self.__files = files
        self.__calendar = calendar

    def set_directory(self, directory):
        self.__directory = directory

    def get_directory(self):
        if self.__directory is None:
            raise RuntimeError("The object doesn't have a directory'")
        return self.__directory

    def set_files(self, files):
        self.__files = files

    def get_files(self):
        return self.__files

    def get_calendar(self):
        return self.__calendar
    
    
    def load_files(self, directory=None):
        if directory != None:
            self.set_directory(directory)
        directory = self.get_directory()
        files = dict()
        for filename in os.listdir(directory):
            files[filename] = docx2txt.process(os.path.join(directory, filename))
        self.set_files(files)

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    reader = Reader(sys.argv[1])
    files = reader.load_files()
    print(reader.get_files())

if __name__ == "__main__":
    main()