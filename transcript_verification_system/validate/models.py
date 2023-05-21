from django.db import models

# Create your models here.
class Transcript(models.Model):
    id          =   models.BigIntegerField(primary_key=True, editable=False, null=False)
    student_id  =   models.BigIntegerField(null=False, editable=False)
    signature   =   models.CharField(max_length=512)
