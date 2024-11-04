from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path('', views.UploadQuestions.as_view(), name='upload'),
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('edit_question/<int:pk>/', views.QuestionUpdateView.as_view(), name='edit_question'),
    path('delete_question/<int:pk>/', views.QuestionDeleteView.as_view(), name='delete_question'),
    path('preview/', views.PreviewQuestions.as_view(), name='preview'),
]
