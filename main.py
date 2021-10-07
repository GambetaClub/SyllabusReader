import sys
import os
import pandas as pd
from docx import Document

class Reader:
    def __init__(self, directory, dates=None, calendar=None):
        self.__directory = directory
        self.__dates = dates
        self.__calendar = calendar

    def set_directory(self, directory):
        if not isinstance(self.__directory, str):
            raise TypeError("Directory must be a str")
        self.__directory = directory

    def get_directory(self):
        return self.__directory

    def get_filenames(self):
        return [key for key in self.__tables.keys()]

    def set_dates(self, dates):
        self.__dates = dates

    def get_dates(self):
        return self.__dates

    def get_calendar(self):
        return self.__calendar

    def recognize_fields(self, df):
        """
        Accepts a dataframe and returns a list of
        weeks, dates, and assignments in their order.
        """
        dates = None
        assignments = None
        if isinstance(df, pd.DataFrame):
            weeks = None
            dates = None
            assignments = None
            if "Assignments" in list(df) or "Week" in list(df) or "Date" in list(df):
                weeks = df["Week"].to_list()
                dates = df["Date"].to_list()
                assignments = df["Assignments"].to_list()
        if not dates:
            return None
        return [weeks, dates, assignments]
        
    def read_docx_table(self, document, table_num=1, n_headers=1):
        """
        Reads a document (docx Document) and returns a nested 
        list with dates and assignments as lists inside. 
        """
        tables = document.tables
        if not tables:
            return None

        tables_data = list()
        for table in tables:
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
            
            table_data = self.recognize_fields(df)
            if table_data:  
                tables_data.append(table_data)
        return tables_data

    def load_dates(self, directory=None):
        """
        Accepts a directory and read_docx_table for each
        single docx file in the directory. At the ends sets
        the sum of the return values of the function as the 
        object table.
        """
        if directory != None:
            self.set_directory(directory)
        dates = dict()
        for filename in os.listdir(self.get_directory()):
            if filename.endswith(".docx"):
                document = Document(os.path.join(sys.argv[1], filename))
                dates[filename] = self.read_docx_table(document)
        self.set_dates(dates)

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    reader = Reader(sys.argv[1])

    reader.load_dates()
    dates = reader.get_dates()
    print(dates)
    # for df in dfs:
    #     print(f"{df}: \n {dfs[df]}")

if __name__ == "__main__":
    main()