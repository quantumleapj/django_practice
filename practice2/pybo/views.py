from django.shortcuts import render,get_object_or_404 , redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import QuestionForm,AnswerForm
from .models import Question, Answer
# Create your views here.

# def index(request):
  # return HttpResponse("안녕하세요 pybo에오신걸 환영합니다")


def index(request):
  """
  pybo 목록 출력
  """

  page = request.GET.get('page','1') 
  question_list = Question.objects.order_by('-create_date')
  paginator = Paginator(question_list,10)
  page_obj = paginator.get_page(page)
  context = {'question_list':page_obj}

  # question_list = Question.objects.order_by('-create_date')
  # context= {'question_list':question_list}

  return render(request, 'pybo/question_list.html',context)

def detail(request, question_id):
  """
  pybo 내용 출력
  """
  # question=Question.objects.get(id=question_id)
  question=get_object_or_404(Question,pk=question_id)
  context = {'question':question}
  return render(request,'pybo/question_detail.html',context)

@login_required(login_url = 'common:login')
def answer_create(request, question_id):
  """
  pybo 답변등록
  """
  question = get_object_or_404(Question, pk=question_id)
  if request.method == "POST":
    form = AnswerForm(request.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.author = request.user
      answer.create_date = timezone.now()
      answer.question = question
      answer.save()
      return redirect('pybo:detail', question_id=question.id)
  else:
    form = AnswerForm()
  context = {'question': question, 'form': form}
  return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
  """
  pybo 질문등록
  """
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    if form.is_valid():
      question = form.save(commit=False)
      print('---------------------')
      print(request.user)
      question.author = request.user
      question.create_date = timezone.now()
      question.save()
      return redirect('pybo:index')
  else:
    form = QuestionForm()
  context = {'form': form}
  return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
  """
  질문수정
  """
  question = get_object_or_404(Question, pk=question_id)
  if request.user != question.author:
    messages.error(request, '수정권한이 없습니다.')
    return redirect('pybo:detail', question_id=question.id)
  if request.method == "POST":
    # 질문 수정을 위해 값 덮어쓰기
    form = QuestionForm(request.POST, instance=question)
    if form.is_valid():
      question = form.save(commit=False)
      question.author = request.user
      question.modify_date = timezone.now() # 수정일시 저장
      question.save()
      return redirect('pybo:detail', question_id=question.id)
  else:
    # 질문 수정 화면에 기존 제목, 내용 반영
    form = QuestionForm(instance=question)
  context = {'form': form}
  return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
  """
  pybo 질문삭제
  """
  question = get_object_or_404(Question, pk=question_id)
  if request.user != question.author:
    messages.error(request, '삭제권한이 없습니다')
    return redirect('pybo:detail', question_id=question.id)
  question.delete()
  return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
  """
  pybo 답변수정
  """
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user != answer.author:
    messages.error(request, '수정권한이 없습니다')
    return redirect('pybo:detail', question_id=answer.question.id)
  if request.method == "POST":
    form = AnswerForm(request.POST, instance=answer)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.author = request.user
      answer.modify_date = timezone.now()
      answer.save()
      return redirect('pybo:detail', question_id=answer.question.id)
  else:
    form = AnswerForm(instance=answer)
  context = {'answer': answer, 'form': form}
  return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
  """
  pybo 답변삭제
  """
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user != answer.author:
    messages.error(request, '삭제권한이 없습니다')
  else:
    answer.delete()
  return redirect('pybo:detail', question_id=answer.question.id)
