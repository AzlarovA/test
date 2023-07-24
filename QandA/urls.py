from django.urls import path
from .views import questions_list, question_detail, question_create, tag_questions, delete

app_name = 'QnA'

urlpatterns = [
    path('', questions_list, name='questions_list'),
    path('question/<int:pk>/', question_detail, name='question_detail'),
    path('question_ask/', question_create, name='question_create'),
    path('genre/<str:slug>/', tag_questions, name='tag_questions'),
    path('delete/<int:pk>/', delete, name='delete'),
]