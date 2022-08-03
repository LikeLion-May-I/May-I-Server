from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'deadline', 'is_send', 'is_expired']
    list_display_links = ['id', 'title']

@admin.register(Apply)
class ApplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'send_date', 'response']
    list_display_links = ['id']
