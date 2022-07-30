import json
from time import timezone
from django.forms import DateTimeField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from models import *

# Create your views here.

def create_interview(request):
    if request=="POST":
        body = json.loads(request.body.decode('utf-8'))
        
        new_interview = Interview.objects.create(
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

def send_interview(request, id):
    if request.method == "GET":
        
        send_interview = get_object_or_404(Interview, pk=id)
        
        send_interview.is_send = 1
        send_interview.save()
        
        new_apply = Apply.objects.create(
            interview = send_interview,
            send_date = timezone.now()
        )
        
        new_apply_json={
            "id" : new_apply.id,
            "send_date" : new_apply.send_date,
            "check_date" : new_apply.check_date,
            "response" : new_apply.response,
            "hold_reason" : new_apply.hold_reason,
        }
        
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
            
            apply.check_date = timezone.now()
            apply.response = body['response']
            apply.hold_reason = body['hold_reason']
            
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
            
            
        
# 시간 카운팅 함수 (제한시간 - 현재시간)

def time_calc(id):
    interview = get_object_or_404(Interview, pk=id)
    
    if interview.is_send == 1:
        currtime = timezone.now()
        time = interview.dealine - currtime
        
        if time < 0 :
            interview.is_expired = 1
        else:
            return time
            
    
    