from rest_framework import serializers
from .models import (
    Comment,
    LikeComment,
    Reply
)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'discussion', 'text', 'created_on']


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = ['id', 'user', 'comment', 'created_at']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'user', 'comment', 'text', 'created_at']
