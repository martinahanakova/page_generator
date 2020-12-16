from django.urls import path

from . import views


app_name = 'page_generator'
urlpatterns = [
    path('questionaire/', views.QuestionaireView.as_view(), name='questionaire'),
    path('start_page/', views.StartView.as_view(), name='start_page'),
    path('page/', views.PageView.as_view(), name='page'),
    path('page_rating/', views.PageRatingView.as_view(), name='page_rating'),
    path('link_page/', views.PageLinkView.as_view(), name='link_page'),
    path('', views.IndexView.as_view(), name='index'),
]
