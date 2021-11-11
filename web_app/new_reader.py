import os
import re
import dateutil.parser
import pandas as pd
from docx import Document

class Reader:
    def __init__(self, dir=None, syllabi=None, calendar=None):
        self.__dir = dir
        self.__syllabi = syllabi
        self.__calendar = calendar

    def set_dir(self, dir):
        self.__dir = dir

    def get_dir(self):
        return self.__dir

    def get_filenames(self):
        return [key for key in self.__tables.keys()]

    def set_syllabi(self, syllabi):
        self.__syllabi = syllabi

    def get_syllabi(self):
        return self.__syllabi

    def get_calendar(self):
        return self.__calendar

    def get_docx_course(self, document):
        """
        Takes a docx (docx.Document) and returns
        the name of course the syllabus belongs to
        """
        # for paragraph in document.paragraphs:
        #     print(paragraph.text)

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

    def insert_to_start(self, assignment, course):
        return course + " - " + assignment

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
        a dictionary of the valid fields of the 
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

    def convert_assignments(self, df, filename):
        """
        Converts the dataframe assignments 
        values to None if the value is either
        only spaces or symbol characters. 
        """
        with pd.option_context('mode.chained_assignment', None):
            df['Assignments'] = df['Assignments'].map(lambda s: self.spec(s))
            df = df[df.Assignments.notnull()]
            df['Assignments'] = df["Assignments"].map(lambda s: self.insert_to_start(s, filename))
            return df

    def recognize_fields(self, df):
        """
        Accepts a dataframe and returns 
        the dataframe only with the fields
        "Assignments", "Week", and "Date".
        """
        if isinstance(df, pd.DataFrame):
            if "Assignments" in list(df) or "Week" in list(df) or "Date" in list(df):
                df = df[["Assignments", "Week", "Date"]]
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

    def get_class_id(self, filename):
        return filename.split(os.sep)[-1]


    def convert_one_docx_to_csv(self, file_path):
        # Gets a docx file (syllabus) and returns
        # a dataframe containing its calendar data
        # f_name = os.path.splitext(file)
        
        if file_path.endswith(".docx"):
            document = Document(file_path)
            df = self.read_docx_table(document)
            df = self.convert_dates(df)
            course_id = self.get_class_id(file_path)
            df = self.convert_assignments(df, course_id)
            # csv = df.to_csv(f"{course_id}.csv", encoding='utf-8', index=False)
            return df
        else:
            return None
