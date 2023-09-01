from user_post.models import Post
from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from user_post.serializers import PostSerializer,RegisterationUserSerializer

# Create your views here.

class RegisterUserAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterationUserSerializer

class PostListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        post_data = Post.objects.all()
        serializer = PostSerializer(post_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post_id_user = self.get_object(pk)
        serializer = PostSerializer(post_id_user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user_obj = self.get_object(pk)
        serializer = PostSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post_id_user = self.get_object(pk)
        post_id_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)