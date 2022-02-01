from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
  return HttpResponse("안녕하세요 pybo에오신걸 환영합니다")