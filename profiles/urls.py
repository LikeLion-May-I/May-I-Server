from django.urls import path

from profiles.views import *

urlpatterns = [
    path('get-profile-one/<int:id>', get_profile_one, name='get_profile_one'),
    path('get-profile-all/<int:category_id>/', get_profile_all, name='get_profile_all'),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout, name="logout"),
    path('get-apply-request-all-for-expert/', get_apply_request_all_for_expert, name='get_apply_request_all_for_expert'),
    path('get-apply-answered-all-for-expert/', get_apply_answered_all_for_expert, name='get_apply_answered_all_for_expert'),
    path('get-apply-request-all-for-reporter/', get_apply_request_all_for_reporter, name='get_apply_request_all_for_reporter'),
    path('get-apply-answered-all-for-reporter/<int:method_id>/', get_apply_answered_all_for_reporter, name='get_apply_answered_all_for_reporter'),

    
]