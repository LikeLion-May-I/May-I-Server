import imp
from unicodedata import name
from django.urls import path

from .models import *
from interviews.views import *
urlpatterns = [
    path('create-interview/<int:id>', create_interview, name="create-interview"),
    path('get-interview-all/', get_interview_all, name="get-interview-all"),
    path('get-interview/<int:id>',get_interview, name="get-interview"),
    path('update-interview/<int:id>', update_interview, name="update-interview"),
    path('delete-interview/<int:id>', delete_interview, name="delete-interview"),
    path('send-interview/<int:interview_id>', send_interview, name="send-interview"),
    path('checked-interview/<int:id>', checked_interview, name="checked-interview"),
    path('update-reply/<int:id>', update_reply, name="update-reply"),
]