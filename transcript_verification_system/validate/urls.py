from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:stud_id>/", views.get_transcript, name="transcript")
]
