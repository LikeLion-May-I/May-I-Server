# Generated by Django 4.0.6 on 2022-08-15 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0003_interview_expert_id_interview_expert_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='amount',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='interview',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='interview/'),
        ),
        migrations.AddField(
            model_name='interview',
            name='purpose',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]