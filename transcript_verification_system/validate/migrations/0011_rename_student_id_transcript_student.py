# Generated by Django 4.2.1 on 2023-05-22 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validate', '0010_student_alter_transcript_student_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transcript',
            old_name='student_id',
            new_name='student',
        ),
    ]
