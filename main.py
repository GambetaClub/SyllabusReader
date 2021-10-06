import sys
import os
import docx2txt

class Reader:
    def __init__(self, directory, files=None, calendar=None):
        self.__directory = directory
        self.__files = files
        self.__calendar = calendar

    def set_directory(self, directory):
        if not isinstance(self.__directory, str):
            raise TypeError("Directory must be a str")
        self.__directory = directory

    def get_directory(self):
        return self.__directory

    def get_filenames(self):
        return [key for key in self.__files.keys()]

    def set_files(self, files):
        if not isinstance(files, dict):
            raise TypeError("Files must be a dict")
        self.__files = files

    def get_files(self):
        return self.__files

    def get_calendar(self):
        return self.__calendar
    
    
    def load_files(self, directory=None):
        if directory != None:
            self.set_directory(directory)
        files = dict()
        for filename in os.listdir(self.get_directory()):
            files[filename] = docx2txt.process(os.path.join(self.get_directory(), filename))
        self.set_files(files)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    reader = Reader(sys.argv[1])

    reader.load_files()

    filenames = reader.get_filenames() # ['Syllabus1.docx', 'Syllabus2.docx', 'Syllabus3.docx']
    
    files = reader.get_files() # { 'Syllabus1.docx': "...", 'Syllabus2.docx': "...", ...}

    print(files[filenames[0]])


if __name__ == "__main__":
    main()