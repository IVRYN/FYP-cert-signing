from django import forms

class GetTranscript(forms.Form):
    student_id  =   forms.CharField(label="Student ID", max_length=11, empty_value="XXXXXXXXXXX")

class ValidateTranscript(forms.Form):
    transcript  =   forms.FileField()
