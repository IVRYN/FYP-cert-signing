from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from django.conf import settings

import random
import hashlib
import os

from .models import Transcript, SubjectInTranscript, Student
from .forms import GetTranscript, ValidateTranscript

# Create your views here.

def get_transcript(request, stud_id):
    transcripts     =   Transcript.objects.filter(student=stud_id)

    return render(request, "validate/transcript.html", {"student_id" : stud_id,
                                                        "transcripts" : transcripts})

def download_transcript(request, transcript_id):
    transcript      =   get_object_or_404(Transcript, pk=transcript_id)
    response        =   HttpResponse(transcript.storage, content_type='application/pdf')
    response['Content-Disposition']     =   f'attachment; filename="{transcript.storage.name}"'
    return response

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
