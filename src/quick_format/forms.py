from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = Quick
        fields =[
            "project_name",
            "comment",
            "file",
        ]

class DeleteQuickForm(forms.ModelForm):
    class Meta:
        model = File
        fields = []