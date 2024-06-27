from django.urls import path
from . import views

urlpatterns = [
    path('discussions/', views.discussion_list_create, name='discussion_list_create'), # 
    path('discussions/<int:pk>/', views.discussion_detail, name='discussion_detail'), # 
    path('discussions/by_tags/', views.discussions_by_tags, name='discussions_by_tags'), 
    path('discussions/search/', views.search_discussions, name='search_discussions'),

    path('likes/', views.like_list_create, name='like_list_create'),
    path('likes/<int:pk>/', views.like_detail, name='like_detail'),
]
