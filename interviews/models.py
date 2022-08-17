from urllib import response
from django.db import models
from profiles.models import User

# Create your models here.

class Interview(models.Model):
    reporter_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    expert_name = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    purpose = models.CharField(max_length=50, null=True, blank=True)
    method = models.IntegerField(null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="interview/", blank=True, null=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_send = models.IntegerField(default=0, null=True, blank=True)
    is_expired = models.IntegerField(default=0, null=True, blank=True)
    expert_id = models.IntegerField(null=True, blank=True)

class Apply(models.Model):
    expert_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, null=True, blank=True)
    send_date = models.DateTimeField(null=True, blank=True)
    check_date = models.DateTimeField(null=True, blank=True)
    response = models.IntegerField(default=0, null=True, blank=True)
    hold_reason = models.CharField(max_length=150, null=True, blank=True)
