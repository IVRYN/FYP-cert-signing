from django.conf import settings
from django.contrib import admin
from django.core.files import File
from pathlib import Path
import os

from .models import Transcript, Subject, SubjectInTranscript, Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class SubjectInTranscriptInline(admin.TabularInline):
    model = SubjectInTranscript

@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'signature', 'date_created']
    inlines = [SubjectInTranscriptInline]

    def sign_transcript(self, obj):
        # transcript = Transcript.objects.filter(id=obj.id)
        # subjects = Transcript.subjects.through.objects.filter(transcript_id=obj.id)

        # Create PDF

        pass

@admin.register(Subject)
class Subject(admin.ModelAdmin):
    list_display = ['id', 'name']
