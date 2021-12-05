from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "syllabi_reader"
urlpatterns = [
    path("", views.index, name="index"),
    path("read_docx", views.read_docx, name="read_docx"),
    path("save_csv", views.save_csv, name="save_csv"),
    path("save_ics", views.save_ics, name="save_ics"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)