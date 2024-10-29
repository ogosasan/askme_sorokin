import copy

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'text for question {i}'
    } for i in range(1, 30)
]

ANSWERS = [
    {
        'id': i,
        'text': f'text for answer {i}'
    } for i in range(1, 15)
]


def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def hot(request):
    HOT_QUESTIONS = copy.deepcopy(QUESTIONS)
    HOT_QUESTIONS.reverse()
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(HOT_QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    one_question = QUESTIONS[question_id - 1]
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(ANSWERS, 5)
    page = paginator.page(page_num)
    return render(request, 'one_question.html', context={
        'question': one_question,
        'answers': page.object_list,
        'page_obj': page
    })


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'register.html')


def search(request, tag):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'search.html',  context={'questions': page.object_list, 'page_obj': page, 'tag':tag})
