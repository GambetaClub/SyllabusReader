import re
import json
import numpy as np
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from new_reader import Reader
from syllabi_reader.models import Document
from syllabi_reader.forms import DocumentForm
from web_app.settings import MEDIA_ROOT
from django.http import HttpResponse
from django.http import FileResponse



# from django.views.decorators.csrf import csrf_exempt, csrf_protect

reader = Reader()

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def get_docx_path(filename):
    """
    Gets the filenae of docx file
    and returns its full path.
    """

    dir = MEDIA_ROOT + "/docx"
    if filename.startswith("~$") or not filename.endswith(".docx"):
        return None
    full_path = dir + "/" + filename
    file_ref = open(full_path, "rb")
    return file_ref.name


def download_file(request, path):
    # fill these variables with real values
    raise NotImplementedError

def get_calendar_df(filename):
    """
    Providing a syllabus name (filename) for a docx file
    the function and returns a dataframe with
    the calendar data of the syllabus.
    """
    file_path = get_docx_path(filename)
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
    calendar = calendar.to_json()
    calendar = json.loads(calendar)
    return calendar
 
def index(request):
    return render(request, "syllabi_reader/index.html", {
        "form": DocumentForm(),
    })

# @csrf_exempt
def read_docx(request):
    if request.is_ajax():
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file.name = format_filename(file.name)
            doc = Document(file = file)
            doc.save()
            calendar = get_calendar_df(file.name)
            doc.delete()
            if calendar is None:
                response = HttpResponse(status=400)
                response.reason_phrase = "Syllabus empty. Make sure the docx file has a table."
                return response
            else:
                calendar = clean_calendar_df(calendar)
                return JsonResponse(calendar, status=200)
        else:
            response = HttpResponse(status=400)
            response.reason_phrase = "Form not valid."
            return response
    else:
        return reverse('syllabi_reader:index')


def save_csv(request):
    if request.method == "POST":
        events = request.POST.get('events', None) # Gets a string representing an array of events
        df = reader.parse_json_events(events) # Parses the string and converts it into a df
        path = reader.convert_df_to_csv(df) # It saves the df as csv file and returns its path
        response = FileResponse(open(path, 'rb'))
        return response
    else:
        return HttpResponseRedirect(reverse("index"))


def save_ics(request):
    if request.method == "POST":
        events = request.POST.get('events', None) # Gets a string representing an array of events
        df = reader.parse_json_events(events) # Parses the string and converts it into a df
        path = reader.convert_df_to_csv(df) # It saves the df as csv file and returns its path
        reader.convert_csv_to_ics(path)
        # response = FileResponse(open(path, 'rb'))
        # return response
        return None
    else:
        return HttpResponseRedirect(reverse("index"))
