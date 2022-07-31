from telnetlib import AUTHENTICATION
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from profiles.models import Profile
from django.contrib.auth.models import update_last_login



# Create your views here.
def get_profile_one(request, id):
    if request.method == "GET":


        profile = get_object_or_404(Profile, pk=id)

        profile_json = {   
            "id": profile.id,
            "name": profile.name,
            "department": profile.department,
            "img": str(profile.img),
            "background": profile.background,
            "office": profile.office,
            "phone": profile.phone,
            "tag": profile.tag,
            "reply_rate": profile.reply_rate,
            "reply_time": profile.reply_time,
            "certification": profile.certification,
            "update_at": profile.update_at,
            "last_login": profile.user.last_login,
        }

        return JsonResponse({
            "status": 200,
            "success": True,
            "message": "전문가 디테일 페이지 업로드 성공",
            "data": profile_json
        })
    
    return JsonResponse({
        "status": 405,
        "success": False,
        "message": "method error",
        "data": None
    })

def get_profile_all(request, category_id):
    if request.method == "GET":

        profile_all = Profile.objects.filter(category_id=category_id)

        profile_all_json = []

        for profile in profile_all:
            profile_json = {
                "id": profile.id,
                "name": profile.name,
                "department": profile.department,
                "img": str(profile.img),
                "tag": profile.tag,
                "reply_rate": profile.reply_rate,
                "reply_time": profile.reply_time,
                "certification": profile.certification,
                "update_at": profile.update_at,
                "last_login": profile.user.last_login,
            }

            profile_all_json.append(profile_json)

        return JsonResponse({
            "status": 200,
            "success": True,
            "message": "전문가 리스트 페이지 업로드 성공",
            "data": profile_all_json
        })

    return JsonResponse({
        "status": 405,
        "success" : False,
        "message": "method error",
        "data": None
    })


# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth import get_user_model
# from interviews.models import *


# def read_interview_for_expert(request):
#     user = authenticate(username="admin", password="1234")
#     login(request, user)

#     # # 원래
#     # user = request.user

#     # 진행

    
#     apply_all = Apply.objects.filter(user=user)
    