# Syllabus Reader


## Our goal
Our goal is to create an easy way for students to add due dates from the syllabi to their calendars. This would be done by simply adding their syllabus to our program. We would then present the due dates to the student on a calendar and allow them to drag and drop different assignments to allow them to have more freedom and fix any mistakes the program could have. We would also allow for the option of manually adding assignments onto the calendar that the program possibly missed, or something the student would like to add, as well as allowing for the deletion of assignments. In order to achieve accuracy with many different types and styles of syllabi, we will have the user select a certain syllabus format that their syllabus is using. Our plan is to make the calendar our starting interface and from there the user could add an entire syllabus or single assignment. We plan on supporting a PDF file type at the start and adding more file types later if we have time.

## Usage
### Install Python
* This can be done through your device's webstore, or from the [Python website](https://www.python.org/downloads/), or even through the terminal by typing `python3`.

### Install Pip
* Once you have Python installed, the next step is to install [pip](https://pypi.org/project/pip/). pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes. To do this, run the command 
* `python3 get-pip.py` in the terminal.

### Download our files from GitHub
* This can be done either by downloading zip, or by cloning the [Git repository](https://github.com/GambetaClub/SyllabusReader).

### Install "requirements.txt"
* Once you have all the previous files installed, run the command 
* `pip3 install -r requirements.txt`

### Add a directory of your syllabi
* Add a directory with your syllabi files. The current version only accepts docx files with tables displaying the calendar inside the files. 

### Run the program
* Run the command, <dir_with_syll> should be the name of the directory with your syllabi inside. 
* `python3 main.py <dir_with_syll>`

### Output
* The current output of the program is an ics file "test.ics" inside the directory you created. You can export this file to your calendar of choice.
* Examples would be [Google Calendar](https://calendar.google.com/) or [iCalendar](https://www.icloud.com/calendar).

