from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Discussion, Like
from .serializers import DiscussionSerializer, LikeSerializer

from comments.models import Comment, LikeComment
from comments.serializers import ReplySerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def discussion_list_create(request):
    match request.method:
        case 'GET':
            discussions = Discussion.objects.all()
            serializer = DiscussionSerializer(discussions, many=True)
            return Response(serializer.data)
        case 'POST':
            serializer = DiscussionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    match request.method:
        case 'GET':
            serializer = DiscussionSerializer(discussion)
            return Response(serializer.data)
        case 'PUT':
            if discussion.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = DiscussionSerializer(discussion, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        case 'DELETE':
            if discussion.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            discussion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def discussions_by_tags(request):
    tags = request.query_params.get('tags', '')
    discussions = Discussion.objects.filter(hashtags__icontains=tags)
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_discussions(request):
    query = request.query_params.get('q', '')
    discussions = Discussion.objects.filter(text__icontains=query)
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def like_list_create(request):
    match request.method:
        case 'GET':
            likes = Like.objects.all()
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)
        case 'POST':
            user = request.user
            discussion_id = request.data.get('discussion')
            like = Like.objects.filter(user=user, discussion_id=discussion_id).first()

            if like:
                # If like exists, unlike it
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                # If like doesn't exist, create it
                serializer = LikeSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def like_detail(request, pk):
    like = get_object_or_404(Like, pk=pk)
    match request.method:
        case 'GET':
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        case 'DELETE':
            if like.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = LikeComment.objects.get_or_create(user=request.user, comment=comment)
    if created:
        return Response(status=status.HTTP_201_CREATED)
    else:
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_to_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    serializer = ReplySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, comment=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
