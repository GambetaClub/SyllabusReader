import sys
import os
import pandas as pd
from docx import Document

class Reader:
    def __init__(self, directory, tables=None, calendar=None):
        self.__directory = directory
        self.__tables = tables
        self.__calendar = calendar

    def set_directory(self, directory):
        if not isinstance(self.__directory, str):
            raise TypeError("Directory must be a str")
        self.__directory = directory

    def get_directory(self):
        return self.__directory

    def get_filenames(self):
        return [key for key in self.__tables.keys()]

    def set_tables(self, tables):
        if not isinstance(tables, dict):
            raise TypeError("tables must be a dict")
        self.__tables = tables

    def get_tables(self):
        return self.__tables

    def get_calendar(self):
        return self.__calendar

    def read_docx_table(self, document, table_num=1, n_headers=1):
        try:
            table = document.tables[-1]
        except IndexError:
            print(f"Document {document} doesn't have any table.")
            return None

        data = [[cell.text for cell in row.cells] for row in table.rows]
        df = pd.DataFrame(data)

        if n_headers == 1:
            df = df.rename(columns=df.iloc [0]).drop (df.index [0]).reset_index(drop=True)
        
        elif n_headers == 2:
            outside_col, inside_col = df.iloc[0], df.iloc [1]
            hier_index = pd.MultiIndex.from_tuples(list (zip(outside_col, inside_col)))
            df = pd.DataFrame(data, columns=hier_index).drop(df.index[[0,1]]).reset_index(drop=True)
    
        elif n_headers > 2:
            print("More than two headers not currently supported")
            df = pd.DataFrame()
        
        return df
    
    def load_tables(self, directory=None):
        if directory != None:
            self.set_directory(directory)
        dfs = dict()
        for filename in os.listdir(self.get_directory()):
            if filename.endswith(".docx"):
                document = Document(os.path.join(sys.argv[1], filename))
                dfs[filename] = self.read_docx_table(document)
        self.set_tables(dfs)

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    reader = Reader(sys.argv[1])

    reader.load_tables()
    dfs = reader.get_tables()
    for df in dfs:
        print(f"{df}: \n {dfs[df]}")

if __name__ == "__main__":
    main()