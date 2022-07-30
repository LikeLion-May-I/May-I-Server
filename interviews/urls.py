import imp
from unicodedata import name
from django.urls import path

from .models import *
from interviews.views import *
urlpatterns = [
    path('create-interview/', create_interview, name="create-interview"),
    path('get-interview-all/', get_interview_all, name="get-interview-all"),
    path('get-interview/<int:id>',get_interview, name="get-interview"),
    path('update-interview/<int:id>', update_interview, name="update-interview"),
    path('delete-interview/<int:id>', delete_interview, name="delete-interview"),
    path('send-interview', send_interview, name="send-interview"),
    path('checked-interview', checked_interview, name="checked-interview"),
]