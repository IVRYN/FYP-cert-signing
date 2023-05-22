from django.contrib import admin

from .models import Transcript, Subject, SubjectInTranscript, Student

# Register your models here.
admin.site.register(Transcript)
admin.site.register(Subject)
admin.site.register(SubjectInTranscript)
admin.site.register(Student)
