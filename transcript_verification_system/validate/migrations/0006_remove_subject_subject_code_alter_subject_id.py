# Generated by Django 4.2.1 on 2023-05-21 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validate', '0005_subject_subject_code_alter_subject_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='subject_code',
        ),
        migrations.AlterField(
            model_name='subject',
            name='id',
            field=models.CharField(default='ABC0000', max_length=10, primary_key=True, serialize=False),
        ),
    ]