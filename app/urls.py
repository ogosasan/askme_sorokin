from django.urls import path
from django.contrib import admin
from app import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('hot/', views.hot, name = 'hot'),
    path('question/<int:question_id>', views.question, name = 'one_question'),
    path('ask/', views.ask, name = 'ask'),
    path('settings/', views.settings, name = 'settings'),
    path('login/', views.login, name = 'login'),
    path('signup/', views.registration, name = 'registration'),
    path('tag/<str:tag>/', views.search, name = 'search'),
    path('admin/', admin.site.urls),
]