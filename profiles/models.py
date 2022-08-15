from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
User=get_user_model()


    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    is_report = models.IntegerField(default = 1, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    img = models.ImageField(upload_to="profile/", blank=True, null=True, default='profile/person.png')
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

    def __str__(self):
        return str(self.user.id) + "/" + self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
