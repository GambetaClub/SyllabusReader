import sys
import os
import re
import pathlib
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

    def check_date(self, d):
        """
        Takes a string date and returns
        the a stringuniform date format if
        possible. Otherwise, it returns None 
        """
        try:
            d = dateutil.parser.parse(d)
            return d
        except:
            return None

    def spec(self, s):
        """
        Takes a string. Returns False is the string is
        made by more than just special characters.
        Otherwise, it returns True.
        """
        if not re.match(r'^[_\W]+$', s) and s != "":
            return s
        else:
            return None

    def check_syllabi(self):
        """
        Set the value of syllabi to be 
        a dictionary of the valid of the 
        documents with a valid format.
        """
        syllabi = self.get_syllabi()
        new_syllabi = dict()
        for key, value in syllabi.items():
            if value is None:
                continue
            new_syllabi[key] = value
        self.set_syllabi(new_syllabi)

    def convert_dates(self, df):
        """
        Convert the dates of the syllabi's
        dataframes into a monotonous format
        and sets the new dictionary for the 
        object attribute.
        """
        df['Date'] = df['Date'].map(lambda d: self.check_date(d))
        df = df[df.Date.notnull()]
        return df 

    def convert_assignments(self,df):
        """
        Converts the dataframe assignments 
        values to None if the value is either
        only spaces or symbol characters. 
        """
        with pd.option_context('mode.chained_assignment', None):
            df['Assignments'] = df['Assignments'].map(lambda s: self.spec(s))
            df = df[df.Assignments.notnull()]
            return df

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
                syllabi[os.path.splitext(filename)[0]] = self.read_docx_table(document)
        self.set_syllabi(syllabi)
        self.check_syllabi()

        syllabi = self.get_syllabi()
        for syllabus in syllabi:
            df = syllabi[syllabus]
            df = self.convert_dates(df)
            df = self.convert_assignments(df)
            syllabi[syllabus] = df
        self.set_syllabi(syllabi)
