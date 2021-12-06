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
                    date = [int(x) for x in row["Date"].split('/')]
                    date = datetime.strptime(str(date[2]) + '-' + str(date[0]) + '-' + str(date[1]), '%Y-%m-%d').strftime('%Y%m%d')
                    event['dtstart'] = date + "T000000Z"
                    self.__calendar.add_component(event)
    
    #uses calendar to create a ICS file
    def exportICS(self):
        file_path = os.path.join(self.__directory, 'calendar.ics')
        f = open(file_path, 'wb')
        f.write(self.__calendar.to_ical())
        f.close()
        return file_path
