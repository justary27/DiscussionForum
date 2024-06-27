from django.urls import path

from . import views

urlpatterns = [
    path('comments/', views.comment_list_create, name='comment_list_create'), #
    path('comments/<int:pk>/', views.comment_detail, name='comment_detail'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comments/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
]