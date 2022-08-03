from django.urls import path

from profiles.views import get_apply_answered_all_for_expert, get_apply_request_all_for_expert, get_apply_one_for_expert, get_profile_all, get_profile_one

urlpatterns = [
    path('get-profile-one/<int:id>', get_profile_one, name='get_profile_one'),
    path('get-profile-all/<int:category_id>/', get_profile_all, name='get_profile_all'),
    path('get-apply-request-all-for-expert/', get_apply_request_all_for_expert, name='get_apply_request_all_for_expert'),
    path('get-apply-answered-all-for-expert/', get_apply_answered_all_for_expert, name='get_apply_answered_all_for_expert'),
    path('get-apply-one-for-expert/<int:id>/', get_apply_one_for_expert, name='get-apply-one-for-expert'),
]