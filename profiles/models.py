from django.db import models

# Create your models here.

class Profile(models.Model):
    #id
    #user
    name = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    img = models.CharField(max_length=100, null=True, blank=True)
    background = models.CharField(max_length=50, null=True, blank=True)
    office = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    reply_rate = models.IntegerField(null=True, blank=True)
    reply_time = models.DateTimeField(auto_now_add=True)
    certification = models.IntegerField(default=0, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True)
    is_email_open = models.IntegerField(default=1, null=True, blank=True)
    is_phone_open = models.IntegerField(default=1, null=True, blank=True)