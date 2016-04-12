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
        # widgets = {
        #     'project_name': forms.ModelChoiceField(queryset=File.objects.all(), empty_label="(Nothing)"),
        # }