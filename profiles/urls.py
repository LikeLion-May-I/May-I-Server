from django.urls import path

from profiles.views import get_profile_all, get_profile_one

urlpatterns = [
    path('get-profile-one/<int:id>', get_profile_one, name='get_profile_one'),
    path('get-profile-all/<int:category_id>/', get_profile_all, name='get_profile_all')
]