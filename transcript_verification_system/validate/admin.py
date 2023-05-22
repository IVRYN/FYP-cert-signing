from django.contrib import admin

from .models import Transcript, Subject, SubjectInTranscript, Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class SubjectInTranscriptInline(admin.TabularInline):
    model = SubjectInTranscript

@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'date_created']
    inlines = [SubjectInTranscriptInline]

class SubjectInline(admin.TabularInline):
    model = Subject
