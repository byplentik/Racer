from django.urls import path

from header import views

urlpatterns = [
    path('', views.HomePageTemplateView.as_view(), name='home'),
    path('vashi-voprosy/', views.QuestionsListView.as_view(), name='questions'),
    path('zadat-vopros/', views.AskQuestionFormView.as_view(), name='zadat_question'),
    path('otzyvy/', views.ReviewsListView.as_view(), name='reviews_view'),
    path('video/', views.VideoTemplateView.as_view(), name='video_view'),
    path('kontakty/', views.ContactsTemplateView.as_view(), name='kontakty_view')
]