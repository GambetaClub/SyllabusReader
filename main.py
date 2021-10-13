import sys
import os
import string
import dateutil.parser
import pandas as pd
from docx import Document

class Reader:
    def __init__(self, directory, syllabi=None, calendar=None):
        self.__directory = directory
        self.__syllabi = syllabi
        self.__calendar = calendar

    def set_directory(self, directory):
        if not isinstance(self.__directory, str):
            raise TypeError("Directory must be a str")
        self.__directory = directory

    def get_directory(self):
        return self.__directory

    def get_filenames(self):
        return [key for key in self.__tables.keys()]

    def set_syllabi(self, syllabi):
        self.__syllabi = syllabi

    def get_syllabi(self):
        return self.__syllabi

    def get_calendar(self):
        return self.__calendar

    def convert_dates(self):
        """
        Convert the dates of the syllabi's
        dataframes into a monotonous format
        and sets the new dictionary for the 
        object attribute.
        """
        syllabi = self.get_syllabi()
        new_syllabi = dict()
        for syllabus in syllabi:
            if syllabi[syllabus] is None:
                continue
            else:
                df = syllabi[syllabus]
                for i, date in enumerate(df["Date"]):
                    try:
                        df["Date"][i] = dateutil.parser.parse(date)
                    except Exception:
                        df["Date"][i] = None

                df = df[df.Date.notnull()]
                new_syllabi[syllabus] = df
        self.set_syllabi(new_syllabi)

    def convert_assignments(self):
        syllabi = self.get_syllabi()
        new_syllabi = dict()
        for syllabus in syllabi:
            if syllabi[syllabus] is None:
                continue
            else:
                df = syllabi[syllabus]
                for i, s in enumerate(df["Assignments"]):
                    print(f"Assignment:\n{s}")
                    if not s.isalnum():
                        df["Assignments"][i] = None

                df = df[df.Assignments.notnull()]
                new_syllabi[syllabus] = df

        self.set_syllabi(new_syllabi)       

    def recognize_fields(self, df):
        """
        Accepts a dataframe and returns 
        the dataframe only with the fields
        "Assignments", "Week", and "Date".
        """
        if isinstance(df, pd.DataFrame):
            if "Assignments" in list(df) or "Week" in list(df) or "Date" in list(df):
                df = df[["Assignments","Week","Date"]]
            else:
                return pd.DataFrame()
        return df
        
    def read_docx_table(self, document, n_headers=1):
        """
        Reads a document's tables (docx Document) and returns 
        a list with dataframes that represent the calendar
        in the syllabus. If the syllabus doesn't contain 
        any table with the format, it returns None. 
        """
        tables = document.tables
        if not tables:
            return None

        dfs = list()
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
            
            df = self.recognize_fields(df)
            if not df.empty:  
                dfs.append(df)
        if not dfs:
            return None
        return dfs[0]

    def load_syllabi(self, directory=None):
        """
        Accepts a directory and reads their tables
        with the calendar information for each
        single docx file in the directory.
        At the end it sets the dataframes as the
        object syllabi.
        """
        if directory != None:
            self.set_directory(directory)
        syllabi = dict()
        for filename in os.listdir(self.get_directory()):
            if filename.endswith(".docx"):
                document = Document(os.path.join(sys.argv[1], filename))
                syllabi[filename] = self.read_docx_table(document)
        self.set_syllabi(syllabi)
        self.convert_dates()
        self.convert_assignments()

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py <directory_name>")
    reader = Reader(sys.argv[1])

    reader.load_syllabi()
    print(reader.get_syllabi())

if __name__ == "__main__":
    main()