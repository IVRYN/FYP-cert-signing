from django.db import models

# Create your models here.
class Subject(models.Model):
    id              =   models.CharField(primary_key=True, max_length=10, editable=True, default="ABC0000")
    name            =   models.CharField(max_length=256, editable=True)

    def __str__(self):
        return f'{self.id} {self.name}'

class Transcript(models.Model):
    id              =   models.BigAutoField(primary_key=True, editable=False, null=False)
    student_id      =   models.ForeignKey("Student", on_delete=models.CASCADE)
    subjects        =   models.ManyToManyField(Subject, through="SubjectInTranscript")
    signature       =   models.CharField(max_length=512, editable=False)
    date_created    =   models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'

class SubjectInTranscript(models.Model):
    id              =   models.BigAutoField(primary_key=True)
    transcript      =   models.ForeignKey("Transcript", on_delete=models.CASCADE)
    subject         =   models.ForeignKey("Subject", on_delete=models.CASCADE)
    marks           =   models.BigIntegerField(editable=True, null=False, default=0)
    grade           =   models.CharField(editable=True, null=False, max_length=2, default="A")

    def __str__(self):
        return f'{self.subject}'

class Student(models.Model):
    id              =   models.BigAutoField(primary_key=True)
    name            =   models.CharField(max_length=256, editable=True)

    def __str__(self):
        return f'{self.name}'
