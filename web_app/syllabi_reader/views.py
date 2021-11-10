from django.http import HttpResponse
from django.shortcuts import render
from new_reader import Reader

from syllabi_reader.models import Document
from syllabi_reader.forms import DocumentForm
from web_app.settings import MEDIA_ROOT
import re

reader = Reader()

def get_calendar_df(filename):
    dir = MEDIA_ROOT + "/docx"
    if filename.startswith("~$") or not filename.endswith(".docx"):
        return None
    full_path = dir + "/" + filename
    file_ref = open(full_path, "rb")
    file_path = file_ref.name
    df = reader.convert_one_docx_to_csv(file_path)
    return df

def format_filename(filename):
    string = re.sub('[^a-zA-Z0-9 \n\.]', '', filename)
    string = string.replace(" ","-")
    return string


def index(request):
    if request.method == 'POST':
        if not request.session["calendar"]:
            request.session["calendar"] = None

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file.name = format_filename(file.name)
            doc = Document(file = file)
            doc.save()
            calendar = get_calendar_df(file.name)
            return render(request, "calendar/index.html", {
                "calendar": calendar,
                "form": form
            })
    else:
        return render(request, "calendar/index.html", {
            "form": DocumentForm(),
        })