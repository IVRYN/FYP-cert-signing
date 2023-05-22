from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Transcript
from .forms import GetTranscript

# Create your views here.

def get_transcript(request, stud_id):
    student_transcript  =   Transcript.objects.get(student_id=stud_id)

    transcript_subjects =   student_transcript.subjectintranscript_set.all()

    return render(request, "validate/transcript.html", {"student_transcript" : student_transcript,
                                                        "subjects" : transcript_subjects})

def index(request):

    if request.method == "POST":
        form = GetTranscript(request.POST)

        if form.is_valid():
            return redirect("transcript", stud_id=form.cleaned_data['student_id'])

    else:
        form = GetTranscript()

    return render(request, "validate/index.html", {"form" : form})
