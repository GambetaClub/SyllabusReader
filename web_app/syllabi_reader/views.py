from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from new_reader import Reader
from syllabi_reader.models import Document
from syllabi_reader.forms import DocumentForm
from web_app.settings import MEDIA_ROOT
import re
import json
import numpy as np

reader = Reader()

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def get_calendar_df(filename):
    """
    Providing a syllabus name (filename)
    the function and returns a dataframe with
    the calendar data of the syllabus.
    """
    dir = MEDIA_ROOT + "/docx"
    if filename.startswith("~$") or not filename.endswith(".docx"):
        return None
    full_path = dir + "/" + filename
    file_ref = open(full_path, "rb")
    file_path = file_ref.name
    df = reader.convert_one_docx_to_csv(file_path)
    return df

def format_filename(filename):
    """
    Gets and string (filename) and 
    returns the same string with no 
    special characthers and substitutes
    ' ' for '-'.
    """
    string = re.sub('[^a-zA-Z0-9 \n\.]', '', filename)
    string = string.replace(" ","-")
    return string

def clean_calendar_df(calendar):
    calendar.reset_index(drop=True, inplace=True)
    calendar['Date'] = calendar['Date'].apply(lambda x: x.strftime("%m/%d/%Y, %H:%M:%S"))
    calendar = calendar.to_json()
    calendar = json.loads(calendar)
    return calendar


 
def index(request):
    if "calendar" not in request.session:
        request.session["calendar"] = []
    return render(request, "calendar/index.html", {
        "form": DocumentForm(),
    })

def read_docx(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file.name = format_filename(file.name)
            doc = Document(file = file)
            doc.save()
            calendar = clean_calendar_df(get_calendar_df(file.name))
            return JsonResponse(calendar)
            # return ({"calendar": json_dump}, status=201)
    else:
        return reverse('syllabi_reader:index')