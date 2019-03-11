from django import forms
from . import models


class UploadForm(forms.Form):
    file = forms.FileField()

    def clean(self):
        return  self.cleaned_data
