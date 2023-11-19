from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def index(request):

    return Response({"Success": "The setup was successful"})

@api_view(['GET'])
def GetAllPosts(request):
    all_posts = Post.objects.all()
    serialized_posts = PostSerializer(all_posts, many=True)
    return Response(serialized_posts.data)

@api_view(['GET', 'POST'])
def CreatePost(request):
    data = request.data
    serialized_data = PostSerializer(data=data)
    if serialized_data.is_valid():
        serialized_data.save()
        return Response({"Successfully": "The post created successfully."}, status=201)
    else:
        return Response(serialized_data.errors, status=400)

@api_view(['DELETE'])
def DeletePost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"Successfully": "The post deleted successfully."}, status=200)
    except Post.DoesNotExist:
        return Response({"Error": "The post dose not exist!"}, status=404)

@api_view(['GET'])
def GetPost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        serialized_post = PostSerializer(data=post)
        return Response(serialized_post.data)
    except Post.DoesNotExist:
        return Response({"Error": "The post dose not exist!"}, status=404)

@api_view(['PUT'])
def UpdatePost(request):
    post_id = request.data.get('post_id')
    new_title = request.data.get('new_title')
    new_content = request.data.get('new_content')
    try:
        post = Post.objects.get(id=post_id)
        if new_title:
            post.title = new_title
        if new_content:
            post.content = new_content
        
        post.save()
        return Response({"Successfully": "The post updated successfully."}, status=200)

    except Post.DoesNotExist:
        return Response({"Error": "The post dose not exist!"}, status=404)
