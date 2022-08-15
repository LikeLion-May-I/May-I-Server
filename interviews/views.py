from datetime import datetime, tzinfo, timedelta
import json
from re import A
from time import timezone
from django.forms import DateTimeField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import pytz
from profiles.models import Profile, User

from .models import *
from profiles.models import *
from rest_framework.authtoken.models import Token

# Create your views here.

def create_interview(request):
    if request.method =="POST":
        body = json.loads(request.body.decode('utf-8'))
        
        token_line = request.META.get('HTTP_AUTHORIZATION')
        token = get_object_or_404(Token, key=token_line)
        
        new_interview = Interview.objects.create(
            reporter_user = token.user,
            title = body['title'],
            method = body['method'],
            body = body['body'],
            url = body['url'],
            deadline = body['deadline'],
            is_send = body['is_send'],
            is_expired = body['is_expired']
        )
        
        new_interview_json = {
            "id" : new_interview.id,
            "reporter_user" : new_interview.reporter_user,
            "title" : new_interview.title,
            "method" : new_interview.method,
            "body" : new_interview.body,
            "url" : new_interview.url,
            "deadline" : new_interview.deadline,
            "is_send" : new_interview.is_send,
            "is_expired" : new_interview.is_expired,
        }
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : 'interview 생성 성공!',
            'data' : new_interview_json
        })

    return JsonResponse({
        'status' : 405,
        'success' : False,
        'message' : 'method error : create_interview',
        'data' : None
    })


def get_interview_all(request):
    if request.method == "GET":
        interview_all = Interview.objects.all()
        
        interview_json_all = []
        
        for interview in interview_all:
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
            interview_json_all.append(interview_json)
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : 'interview_all 수신 성공!',
            'data' : interview_json_all
        })
        
    return JsonResponse({
        'status' : 405,
        'success' : False,
        'message' : 'method error : get_interview_all',
        'data' : None
    })
    
def get_interview(request, id):
    if request.method == "GET":
        interview= get_object_or_404(Interview, pk=id)
        
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
    
def update_interview(request, id):
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_interview = get_object_or_404(Interview, pk=id)
        
        update_interview.title = body['title']
        update_interview.method = body['method']
        update_interview.body = body['body']
        update_interview.url = body['url']
        update_interview.deadline = body['deadline']
        update_interview.is_send = body['is_send']
        update_interview.is_expired = body=['is_send']
        update_interview.is_expired = body['is_expired']
        
        update_interview.save()
        
        update_interview_json = {
            "id" : update_interview.id,
            "title" : update_interview.title,
            "method" : update_interview.method,
            "body" : update_interview.body,
            "url" : update_interview.url,
            "deadline" : update_interview.deadline,
            "is_send" : update_interview.is_send,
            "is_expired" : update_interview.is_expired,
        }
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '업데이트 성공!',
            'data' : update_interview_json
        })
        
    return JsonResponse({
        'status' : 405,
        'success' : True,
        'message' : 'method error : update_interview',
        'data' : None
    })

def delete_interview(request, id):
    if request.method == "DELETE":
        delete_interview = get_object_or_404(Interview, pk=id)
        
        delete_interview.delete()
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : 'interview 삭제 성공!',
            'data' : None
        })
    return JsonResponse({
        'status' : 405,
            'success' : False,
            'message' : 'method error : delete_interview',
            'data' : None
    })

# 임시저장 -> 진짜 인터뷰 보내기
# 이 때는 설정해 둔 deadline과 별개로 따로 시간 counting은 하지 않습니다
# 인터뷰 제안서가 넘어감과 동시에 apply가 생겨요
# 헤더에 expert 관련 정보를 줘야 합니다

def send_interview(request, interview_id):
    if request.method == "GET":
        
        token_line = request.META.get('HTTP_AUTHORIZATION')
        token = get_object_or_404(Token, key=token_line)
        
        new_apply = Apply.objects.create(
            expert_user = token.user,
            interview = get_object_or_404(Interview, pk=interview_id),
        )
        
        new_apply_json={
            "id" : new_apply.id,
            "expert_user" : new_apply.expert_user,
            "send_date" : new_apply.send_date,
            "check_date" : new_apply.check_date,
            "response" : new_apply.response,
            "hold_reason" : new_apply.hold_reason,
        }
        
        new_apply.interview.is_send = 1
        new_apply.interview.save()
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '전송 성공!',
            'data' : new_apply_json
        })
        
    return JsonResponse({
        'status' : 405,
        'success' : False,
        'message' : 'method error : send_interview',
        'data' : None
    })


# expert가 수락/보류/거절 눌렀을 때 checkdate update + response 저장 + hold_reason까지 저장

def checked_interview(request, id):
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        checked_interview = get_object_or_404(Interview, pk=id)
        
        if checked_interview.is_expired == 0:
            apply = checked_interview.apply
            
            apply.check_date = datetime.now()
            apply.response = body['response']
            apply.hold_reason = body['hold_reason']
            # 프런트에서 공백으로라도 보내주기!!
            
            apply.save()
            
            apply_json = {
                "id" : apply.id,
                "send_date" : apply.send_date,
                "check_date" : apply.check_date,
                "response" : apply.response,
                "hold_reason" : apply.hold_reason,
            }
            
            return JsonResponse({
                'status' : 200,
                'success' : True,
                'message' : 'apply 업데이트 성공',
                'data' : apply_json
            })

        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : 'is_expired == True',
            'data' : None
        })
            
#timedelta 값 int로 바꿔주는 함수 - 이 함수로 바꿔주면 정수형들과 연산이 가능해요.

def timedelta2int(td):
    res = round(td.microseconds/float(1000000)) + (td.seconds + td.days * 24 * 3600)
    return res
            
        
# 시간 카운팅 함수 (제한시간 - 현재시간)
# 초 단위 출력

def time_calc(id):
    interview = get_object_or_404(Interview, pk=id)
    
    if interview.is_send == 1:
        KST = pytz.timezone('Asia/Seoul')
        
        currtime = datetime.now().astimezone(KST)
        deadline = interview.deadline.astimezone(KST)
        
        time = deadline - currtime
        time = timedelta2int(time)
        
        if time < 0 :
            interview.is_expired = 1
            # apply = interview.apply
            # expert_profile = get_object_or_404(Profile, user=apply.expert_user)
            # expert_profile.reply_rate = reply_rate(apply.expert_user)
            # expert_profile.save()
            return 0
        else:
            return time

# 평균 응답률 - 전문가에 따름


def reply_rate(id):
   
    expert = get_object_or_404(User, pk=id)

    apply_all = Apply.objects.filter(expert_user=expert)
    
    totalNum = 0
    repliedNum = 0
    for apply in apply_all:
        if apply.interview.is_expired == 1:
            totalNum += 1

            if apply.response != 0:
                repliedNum += 1


    

        
        
    
    reply_rate = int(float(repliedNum / totalNum) * 100)
    
    return reply_rate


# 평균 응답 시간 - 전문가에 따름
# totalTime - 초 단위

def reply_time(request, id):
    if request.method == "GET":
        user = get_object_or_404(User, pk=id)
        apply_all = Apply.objects.filter(expert_user=user)
        
        repliedNum = 0
        totalTime = 0
        
        for apply in apply_all:
            if apply.response != 0:
                repliedNum += 1
                totalTime += timedelta2int(apply.check_date - apply.send_date)
        
        reply_time = (totalTime / repliedNum)/3600
        
        reply_time_json = {
            "totalNum" : repliedNum,
            "totalTime" : totalTime,
            "reply_time" : reply_time,
        }
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            "message" : "평균응답시간 계산 성공",
            "data" : reply_time_json
        })
        
    return JsonResponse({
        'status' : 405,
        'success' : False,
        "message" : "method error : reply_time",
        'data' : None,   
    })
                
        
