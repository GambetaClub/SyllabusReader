import os
import re
from ics_converter import ICSConverter
import pathlib
import dateutil.parser
import pandas as pd
from docx import Document

class Reader:
    def __init__(self, directory=None, syllabi=None, calendar=None):
        self.__directory = directory
        self.__syllabi = syllabi
        self.__calendar = calendar

    def set_directory(self, directory):
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
        dir_name = self.get_directory()
        for filename in os.listdir(dir_name):
            if filename.endswith(".docx"):
                document = Document(os.path.join(dir_name, filename))
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

    def get_files_dir(self, args):
        files_dir = pathlib.Path().resolve()
        if len(args) == 2:
            files_dir = os.path.join(files_dir, args[1])
        else:
            print("What's the directory's name in which the csv files are?")
            print("Press enter if it's in the current directory.")
            dir_name = input()
            files_dir = os.path.join(files_dir, dir_name)
        return files_dir

    def convert_docx_to_cvs(self, files_dir):
        reader = Reader()
        reader.set_directory(files_dir)
        reader.load_syllabi()
        syllabi = reader.get_syllabi()
        for syllabus in syllabi:
            syllabi[syllabus].to_csv(f"{syllabus}.csv", encoding='utf-8', index=False)

    def convert_csv_to_ics(self, files_dir):
        converter = ICSConverter(files_dir)
        csv_filenames = [filename for filename in os.listdir(files_dir) if filename.endswith('.csv')]
        if csv_filenames:
            for filename in csv_filenames:
                converter.readCSV(f"{filename}")
                converter.exportICS()
        else:
            print("There are no csv files in the listed directory.")
            return False

    def display_interface(self, args):
        print("Options:")
        print(f"1: Convert docx to csv format.")
        print(f"2: Convert csv to ics format.")
        print(f"3: Convert docx to ics format.")
        option = input()
        files_dir = self.get_files_dir(args)
        
        if option == '1':
            try:
                self.convert_docx_to_cvs(files_dir)
                print("The docx files were converted to csv successfully.")
            except:
                print("The docx files could not be converted to csv.")
        elif option == '2':
            try:
                self.convert_csv_to_ics(files_dir)
            except:
                print("The csv files could not be converted to ics.")
        elif option == '3':
            try:
                self.convert_csv_to_ics(files_dir)
                self.convert_docx_to_cvs(files_dir)
            except: 
                print("Failed in doing both.")
        else:
            print("Invalid option")
