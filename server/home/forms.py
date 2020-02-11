from django import forms

class FileForm(forms.Form):
    name = forms.CharField(max_length=500)
    file = forms.FileField()