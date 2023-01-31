from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plan
import json
from django.core import serializers


@csrf_exempt
def main(request:HttpRequest,*args, **kwargs):
  plans = Plan.objects.all()
  context = {'plans': plans}
  return render(request, "test_main.html", context=context)
  

#일정 생성 함수
#POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def create(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    newPlan = Plan(startTime = req['startTime'], endTime = req['endTime'], location = req['location'], title = req['title'], content = req['content'])
    newPlan.save()
    context = {'newPlan': newPlan}
    return JsonResponse({})


#일정 수정 함수
#POST로 넘어온 데이터로 updatedPlan 모델 객체 저장
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def update(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    pk = req['id']
    updatedPlan = Plan.objects.all().get(id=pk)
    updatedPlan.startTime = req['startTime']
    updatedPlan.endTime = req['endTime']
    updatedPlan.location = req['location']
    updatedPlan.title = req['title']
    updatedPlan.content = req['content']
    updatedPlan.save()
    context = {'updatedPlan': updatedPlan}
    return JsonResponse({})


#일정 생성 함수
#POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def retrieve(request, *args, **kwargs):
  plans = serializers.serialize('json', Plan.objects.all())
  return JsonResponse({'plans': plans})


#일정 삭제 함수
#POST로 넘어온 id값으로 객체 삭제
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def delete(request, *args, **kwargs):
  if request.method == 'POST':
    pk = json.loads(request.body)['id']
    Plan.objects.all().get(id=pk).delete()
  return JsonResponse({})
  

#일정 상세보기 함수
#delete 테스트를 위해 임시로 넣은 함수
def detail(request, pk, *args, **kwargs):
  plan = Plan.objects.all().get(id=pk)
  
  startTime = str(plan.startTime)
  print(startTime.split(" "))
  context = {'plan': plan}
  return render(request, 'test_detail.html', context=context)
