from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list_create, name='user_list_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/search/', views.user_search, name='user_search'),
    path('users/follow/<int:user_id>/', views.follow_user, name='follow_user'),
]
