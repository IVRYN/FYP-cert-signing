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
    list_display = ['id', 'student_id', 'signature', 'date_created']
    inlines = [SubjectInTranscriptInline]

    def save_model(self, request, obj, form, change):
        obj.user    =   request.user

        # signature = sign_transcript(obj)

        super().save_model(request, obj, form, change)

    def sign_transcript(self, obj):
        # transcript = Transcript.objects.filter(id=obj.id)
        # subjects = Transcript.subjects.through.objects.filter(transcript_id=obj.id)

        # Create PDF

        pass

@admin.register(Subject)
class Subject(admin.ModelAdmin):
    list_display = ['id', 'name']
