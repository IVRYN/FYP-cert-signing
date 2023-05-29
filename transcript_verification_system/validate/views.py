from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.conf import settings

import random
import hashlib
import os

from .models import Transcript, SubjectInTranscript, Student
from .forms import GetTranscript, ValidateTranscript

# Create your views here.

def get_transcript(request, stud_id):
    student_transcript  =   Transcript.objects.filter(student_id=stud_id)

    transcript_ids      =   []
    for x in range(student_transcript.count()):
        transcript_ids.append(student_transcript[x].id)

    transcript_subject  =   []
    for x in range(student_transcript.count()):
        transcript_subject.append(SubjectInTranscript.objects.filter(transcript_id=student_transcript[x].id))

    #transcript_subjects =   student_transcript.subjectintranscript_set.all()

    return render(request, "validate/transcript.html", {"student_id" : stud_id,
                                                        "transcript_id" : transcript_ids,
                                                        "transcript_subjects" : transcript_subject})

def index(request):

    if request.method == "POST":
        form = GetTranscript(request.POST)

        if form.is_valid():
            return redirect("transcript", stud_id=form.cleaned_data['student_id'])

    else:
        form = GetTranscript()

    return render(request, "validate/index.html", {"form" : form})

def validate_transcript(request):
    if request.method == "POST":
        form = ValidateTranscript(request.POST, request.FILES)

        if form.is_valid():
            transcript_sig = file_handling(request.FILES['transcript'])

            return redirect("validate_status", signature=transcript_sig)

        return redirect("validate_transcript")
    else:
        form = ValidateTranscript()

        return render(request, "validate/validation.html", {"form" : form})

def validate_status(request, signature):
    transcript  =   Transcript.objects.filter(signature=signature)
    status      =   transcript.exists()

    if status:
        student =   Student.objects.get(id=transcript[0].student_id)
    else:
        student =   {'id' : 'Not Found', 'name' : 'Not Found'}

    return render(request, "validate/status.html", {"signature" : signature,
                                                    "transcript" : transcript,
                                                    "student"   : student,
                                                    "status" : status
                                                    })

# Handle the verification files
def file_handling(file):
    signature = hashlib.sha256(file.read()).hexdigest()
    return signature
