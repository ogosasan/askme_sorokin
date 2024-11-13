import copy

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render
from app.models import Question, Answer, QuestionLike, QuestionManager, Tag



def index(request):
    questions = Question.objects.newest()
    page = pagination(request, questions)
    tags = Tag.objects.all()[:9]
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page, 'tags': tags})


def hot(request):
    questions = Question.objects.hot()
    page = pagination(request, questions)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    try:
        question_id = int(question_id)
        if question_id <= 0:
            raise IndexError
        one_question = Question.objects.filter(id=question_id).first()
    except (ValueError, IndexError):
        raise Http404("Question not found")
    tags = one_question.tags.all()
    answers = Answer.objects.filter(question=one_question)
    page = pagination(request, answers)
    return render(request, 'one_question.html', context={
        'question': one_question,
        'answers': page.object_list,
        'page_obj': page,
        'tags': tags
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
    questions = Question.objects.filter(tags__name=tag)
    page = pagination(request, questions)
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
