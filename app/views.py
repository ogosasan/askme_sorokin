import copy

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
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
    page = pagination(request, QUESTIONS)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def hot(request):
    HOT_QUESTIONS = copy.deepcopy(QUESTIONS)
    HOT_QUESTIONS.reverse()
    page = pagination(request, HOT_QUESTIONS)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    try:
        question_id = int(question_id)
        if question_id <= 0 or question_id > len(QUESTIONS):
            raise IndexError
        one_question = QUESTIONS[question_id - 1]
    except (ValueError, IndexError):
        raise Http404("Question not found")

    page = pagination(request, ANSWERS)
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
    page = pagination(request, QUESTIONS)
    return render(request, 'search.html', context={'questions': page.object_list, 'page_obj': page, 'tag': tag})


def pagination(request, base):
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1
    paginator = Paginator(base, 5)
    try:
        page = paginator.page(page_num)
    except (EmptyPage, PageNotAnInteger):
        page = paginator.page(1)

    return page
