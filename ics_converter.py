import os
import csv
import re
from icalendar import Calendar, Event
from datetime import datetime
from pathlib import Path

class ICSConverter:
    def __init__(self, directory):
        self.__calendar = Calendar()
        self.__calendar.add("version", "2.0")
        self.__directory = directory

    #reads the CSV file and adds events to the calendar
    def readCSV(self, file):
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line = 0
            for row in csv_reader:
                line += 1
                if row["Assignments"] != '-' and row['Assignments'] != '':
                    event = Event()
                    event.add("summary", row["Assignments"])
                    date = [int(x) for x in re.split(r'-| |\:', row["Date"])]
                    date = str(datetime(date[0], date[1], date[2]).date()).split('-')
                    event['dtstart'] = date[0] + date[1] + date[2] + "T000000Z"
                    self.__calendar.add_component(event)
    
    #uses calendar to create a ICS file
    def exportICS(self):
        f = open(os.path.join(self.__directory, 'test.ics'), 'wb')
        f.write(self.__calendar.to_ical())
        f.close()
