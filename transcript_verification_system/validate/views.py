from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Transcript, SubjectInTranscript
from .forms import GetTranscript

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
