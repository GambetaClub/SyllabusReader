import sys
from pathlib import Path

class Reader:
    def __init__(self, directory, files=None, calendar=None):
        self.directory = directory
        self.files = files
        self.calendar = calendar
    
    def load_files(self, directory):
        files = {}
        for child in Path(directory).iterdir():
            if child.is_file():
                files[child.name] = child.read_text()
        return files

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <filename>")
        

if __name__ == "__main__":
    main()