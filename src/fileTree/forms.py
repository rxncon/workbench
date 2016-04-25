from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields =[
            "project_name",
            "comment",
            "file",
        ]

class DeleteFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = []