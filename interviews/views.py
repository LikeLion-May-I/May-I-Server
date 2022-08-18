import json
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from profiles.models import Profile, User

from .models import *
from profiles.models import *
from rest_framework.authtoken.models import Token

# Create your views here.

def create_interview(request, id):
    if request.method =="POST":
        
        token_line = request.META.get('HTTP_AUTHORIZATION')
        token = get_object_or_404(Token, key=token_line)
        
        expert_user = get_object_or_404(User, pk=id)
        

        new_interview = Interview.objects.create(
            reporter_user = token.user,
            expert_name = expert_user.profile.name,
            expert_id = id,
        )
        
        new_interview_json = {
            "id" : new_interview.id,
            "reporter_user" : new_interview.reporter_user.profile.name,
            "expert_name"   : new_interview.expert_name,
            "expert_id"     : id,
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
        
        token_line = request.META.get('HTTP_AUTHORIZATION')
        token = get_object_or_404(Token, key=token_line)
        
        interview_all = Interview.objects.all()
        interview_json_all = []
        
        for interview in interview_all:

            interview_json=interview_json = {
                "id"            : interview.id,
                "reporter_user" : interview.reporter_user.profile.name,
                "is_report"     : token.user.profile.is_report,
                "expert_name"   : interview.expert_name,
                "title"         : interview.title,
                "purpose"       : interview.purpose,
                "method"        : interview.method,
                "amount"        : interview.amount,
                "body"          : interview.body,
                "url"           : interview.url,
                "deadline"      : interview.deadline,
                "is_send"       : interview.is_send,
                "is_expired"    : interview.is_expired,
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

        token_line = request.META.get('HTTP_AUTHORIZATION')
        token = get_object_or_404(Token, key=token_line)
        
        interview= get_object_or_404(Interview, pk=id)
        

        interview_json = {
            "id"            : interview.id,
            "reporter_user" : interview.reporter_user.profile.name,
            "is_report"     : token.user.profile.is_report,
            "expert_name"   : interview.expert_name,
            "title"         : interview.title,
            "department": interview.reporter_user.profile.department,
            "purpose"       : interview.purpose,
            "method"        : interview.method,
            "amount"        : interview.amount,
            "body"          : interview.body,
            "url"           : interview.url,
            "deadline"      : interview.deadline,
            "is_send"       : interview.is_send,
            "is_expired"    : interview.is_expired,
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
    if request.method == "POST":
        
        # 이미지 파일이 있으므로 request에서 구분하여 받기
        body =  request.POST
        if request.FILES:
            file = request.FILES['file']
        else : file = None

        
        update_interview = get_object_or_404(Interview, pk=id)
      
        update_interview.title = body['title']
        update_interview.purpose = body['purpose']
        update_interview.method = body['method']
        update_interview.amount = body['amount']
        update_interview.body = body['body']
        update_interview.file = file
        update_interview.url = body['url']
        update_interview.deadline = body['deadline']

        update_interview.save()
        
        update_interview_json = {
            "id"            : update_interview.id,
            "reporter_user" : update_interview.reporter_user.profile.name,
            "expert_name"   : update_interview.expert_name,
            "title"         : update_interview.title,
            "purpose"       : update_interview.purpose,
            "method"        : update_interview.method,
            "amount"        : update_interview.amount,
            "body"          : update_interview.body,
            "url"           : update_interview.url,
            "deadline"      : update_interview.deadline,
            "is_send"       : update_interview.is_send,
            "is_expired"    : update_interview.is_expired,
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
# 인터뷰 제안서가 넘어감과 동시에 create_apply
# 헤더에 expert 관련 정보를 줘야 합니다

def send_interview(request, interview_id):
    if request.method == "POST":
        
        send_interview = get_object_or_404(Interview, pk=interview_id)
        
        new_apply = Apply.objects.create(
            interview = send_interview,
            expert_user = get_object_or_404(User, pk=send_interview.expert_id),
            send_date = datetime.now()
        )

        new_apply_json={
            "id" : new_apply.id,
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
# 이때 apply_update

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
            'status' : 400,
            'success' : False,
            'message' : 'is_expired == True',
            'data' : None
        })
            
#timedelta 값 int로 바꿔주는 함수 - 이 함수로 바꿔주면 정수형들과 연산이 가능해요.

def timedelta2int(td):
    res = round(td.microseconds/float(1000000)) + (td.seconds + td.days * 24 * 3600)
    return res
            
        
# deadline - 현재시간 == 0 : 인터뷰 상태, 응답률, 응답시간 업데이트

def update_reply(request, id):
    if request.method == "PATCH":
        interview = get_object_or_404(Interview, pk=id)
    
        interview.is_expired = 1
        expert_profile = get_object_or_404(Profile, user=interview.apply.expert_user)
        expert_profile.reply_rate = reply_rate(expert_profile.user.id)
        expert_profile.reply_time = reply_time(expert_profile.user.id)
        
        expert_profile.save()

        reply_json = {
            "expert_id" : expert_profile.user.id,
            "reply_rate" : expert_profile.reply_rate,
            "reply_time" : expert_profile.reply_time, 
        }
        
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : 'update-reply 성공',
            'data' : reply_json
        })
        


# 평균 응답률 - 전문가에 따름
# deadline 지난 것들 기준

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
                
    if totalNum != 0:
        reply_rate = int(float(repliedNum / totalNum) * 100)
    else:
        reply_rate = -1
    
    return reply_rate


# 평균 응답 시간 - 전문가에 따름
# totalTime - 초 단위
# deadline 지난 것들 기준으로

def reply_time(id):
    
    user = get_object_or_404(User, pk=id)
    apply_all = Apply.objects.filter(expert_user=user)
    
    repliedNum = 0
    totalTime = 0
    
    for apply in apply_all:
        if apply.interview.is_expired == 1:
            if apply.response != 0:
                repliedNum += 1
                totalTime += timedelta2int(apply.check_date - apply.send_date)
    
    if repliedNum != 0:
        reply_time = (totalTime / repliedNum)/3600
    else:
        reply_time = -1
    
    return reply_time
                
        
