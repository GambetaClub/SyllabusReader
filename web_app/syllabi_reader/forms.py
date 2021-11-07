from django import forms

class DocumentForm(forms.Form):
    file = forms.FileField()
    file.widget.attrs.update({'id': 'file_input', 'accept': '.docx', 'label': ''})

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ""
