from django.urls import path

from header import views

urlpatterns = [
    path('', views.HomePageTemplateView.as_view(), name='home'),
    path('vashi-voprosy/', views.QuestionsListView.as_view(), name='questions'),
    path('zadat-vopros/', views.AskQuestionFormView.as_view(), name='zadat_question'),
]