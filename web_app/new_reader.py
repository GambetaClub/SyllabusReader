import os
import re
import dateutil.parser
import json 
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
        raise NotImplementedError

    def check_date(self, d):
        """
        Takes a string date and returns
        the a string uniform date format if
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
        df['Date'] = df['Date'].apply(lambda x: x.strftime("%m/%d/%Y"))
        return df 

    def convert_assignments(self, df, filename):
        """
        Converts the dataframe assignments values to None
        if the value is either only spaces or symbol characters. 
        """
        with pd.option_context('mode.chained_assignment', None):
            df['Assignments'] = df['Assignments'].map(lambda s: self.spec(s))
            df = df[df.Assignments.notnull()]
            df['Assignments'] = df["Assignments"].map(lambda s: self.insert_to_start(s, filename))
            return df

    def recognize_fields(self, df):
        """
        Accepts a dataframe and returns the dataframe only with the fields
        "Assignments" and "Date". If the dataframe doesn't contain
        the fields, it returns an empty dataframe.
        """
        if isinstance(df, pd.DataFrame):
            if "Assignments" in list(df) or "Date" in list(df):
                df = df[["Assignments", "Date"]]
            else:
                return pd.DataFrame()
        return df
        
    def read_docx_table(self, document, n_headers=1):
        """
        Reads a document's tables (docx Document) and returns 
        a with dataframe that represent the calendar
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

    def get_class_name(self, full_path):
        """
        Returns the name of the last file of an
        absolute path without the file extension.
        """
        return full_path.split(os.sep)[-1].rsplit('.', 1)[0]


    def convert_one_docx_to_csv(self, file_path):
        """
        Gets a docx file (syllabus) and returns
        a dataframe containing its calendar data
        f_name = os.path.splitext(file)
        """
        
        if file_path.endswith(".docx"):
            document = Document(file_path)
            df = self.read_docx_table(document)
            if df is None:
                return None
            df = self.convert_dates(df)
            class_name = self.get_class_name(file_path)
            df = self.convert_assignments(df, class_name)
            return df
        else:
            return None


    def parse_json_events(self, str_events): 
        """
        Accepts a string representing an array of events.
        It converts the string to a dataframe in the format 
        used in the class. It returns the dataframe in the 
        final format.
        """
        events = json.loads(str_events)
        length = len(events)
        arr_events = []
        for i in range(length):
            assignment = events[i]["description"]
            date = str(str(events[i]["date"][0]) + '/' + str(events[i]["date"][1]) + '/' + str(events[i]["date"][2]))
            event = [assignment, date]
            arr_events.append(event)
        df = pd.DataFrame(data=arr_events)
        df = df.rename(columns={0: 'Assignments', 1: 'Date'})

        # The following line prompts an error.
        # I was trying to use it so the dates would be
        # formatted the same way the reader does it at the 
        # time of reading a word document. 
        # df = self.convert_dates(df)
        
        return df

    def convert_df_to_csv(self, df):
        if df is not None:
            csv = df.to_csv(f"calendar.csv", encoding='utf-8', index=False)