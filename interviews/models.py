from urllib import response
from django.db import models

# Create your models here.

class Interview(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    method = models.IntegerField(null=True, blank=True)
    body = models.CharField(max_length=500, null=True, blank=True)
    # filefield
    url = models.URLField(max_length=500)
    deadline = models.DateTimeField()
    is_send = models.IntegerField(default=0, null=True, blank=True)
    is_expired = models.IntegerField(default=0, null=True, blank=True)

class Apply(models.Model):
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, null = True)
    send_date = models.DateTimeField(default="", null=True, blank=True)
    check_date = models.DateTimeField(default="", null=True, blank=True)
    response = models.IntegerField(default=0, null=True, blank=True)
    hold_reason = models.CharField(max_length=150, null=True, blank=True)