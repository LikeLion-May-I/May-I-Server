from time import time
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from interviews.models import Apply

from profiles.models import Profile
from django.contrib.auth import get_user_model, authenticate, login, logout
from interviews.views import *
from django.utils import timezone
from datetime import datetime

from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile


User=get_user_model()


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

        token_line = request.META.get('HTTP_AUTHORIZATION')

        # token_line = 너가 원하는 유저의 토큰 스트링으로 넣어두기
        token = get_object_or_404(Token, key=token_line)
        print(token.user.id)

        
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

# def time_calc_2(interview):

#     if interview.is_send == 1:
#         currtime = datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None)
#         time = interview.deadline - currtime

#         if time.minutes > 0:
#             interview.is_expired = 1
#         else:
#             return time


def get_apply_request_all_for_expert(request):
    if request.method == "GET":

        user = authenticate(username="sanbo", password="userexpert")
        login(request, user)

        apply_all = Apply.objects.filter(expert_user=user)
    
        apply_all_json = []

        for apply in apply_all:

            if apply.response == 0:

                sender_profile = get_object_or_404(Profile, user=apply.interview.reporter_user)

                apply_json = {
                    "id": apply.id,
                    "department": sender_profile.department,
                    "title": apply.interview.title,
                    # "deadline": time_calc_2(apply.interview),
                    "status": apply.interview.is_expired
                }

                apply_all_json.append(apply_json)

        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '전문가 마이페이지 요청 인터뷰 불러오기 성공 !',
            'data' : apply_all_json
        })

    return JsonResponse({
        "status": 405,
        "success" : False,
        "message": "method error",
        "data": None
    })

def get_apply_answered_all_for_expert(request):
    if request.method == "GET":

        user = authenticate(username="sanbo", password="userexpert")
        login(request, user)

        apply_all = Apply.objects.filter(expert_user=user)
    
        apply_all_json = []

        for apply in apply_all:
            if apply.response > 0:
                sender_profile = get_object_or_404(Profile, user=apply.interview.reporter_user)

                apply_json = {
                    "id": apply.id,
                    "department": sender_profile.department,
                    "title": apply.interview.title,
                    "status": apply.response,
                }
                apply_all_json.append(apply_json)

        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '전문가 마이페이지 인터뷰 현황 불러오기 성공 !',
            'data' : apply_all_json
        })

    return JsonResponse({
        "status": 405,
        "success" : False,
        "message": "method error",
        "data": None
    })

def get_apply_one_for_expert(request, id):

    if request.method == "GET":

        apply = get_object_or_404(Apply, pk=id)
        interview = apply.interview
    
        interview_json={
                "id" : interview.id,
                "title" : interview.title,
                "method" : interview.method,
                "body" : interview.body,
                "url" : interview.url,
                "deadline" : interview.deadline,
                "is_send" : interview.is_send,
                "is_expired" : interview.is_expired,
            }
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : 'interview 수신 성공!',
            'data' : interview_json
        })
        
    return JsonResponse({
        'status' : 405,
        'success' : False,
        'message' : 'method error : get_interview',
        'data' : None
    })




#######################################################
#######################drf#############################
#######################################################


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def patch(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # data = serializer.validated_data
        # profile.nickname = data['name']
        # profile.position = data['department']
        # profile.subjects = data['background']
        # if request.data['image']:
        #     profile.image = request.data['image']
        profile.save()
        return Response({"result": "ok"},
                        status=status.HTTP_206_PARTIAL_CONTENT)

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
        