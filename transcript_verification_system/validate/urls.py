from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("validate", views.validate_transcript, name="validate_transcript"),
    path("validate/<str:signature>", views.validate_status, name="validate_status"),
    path("<int:stud_id>/", views.get_transcript, name="transcript")
]
