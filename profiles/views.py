from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from profiles.models import Profile
from django.contrib.auth.models import update_last_login

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
